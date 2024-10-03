import torch
import torch.nn as nn
from torch import Tensor
import torch.nn.functional as F
from typing import Optional, Dict, Tuple, List
from codeformer_kit.utils import get_root_logger
from codeformer_kit.utils.registry import ARCH_REGISTRY


def normalize(in_channels: int) -> nn.GroupNorm:
    """
    Returns a GroupNorm layer with 32 groups, designed to normalize the input.

    Args:
        in_channels (int): The number of input channels for the normalization.

    Returns:
        nn.GroupNorm: A GroupNorm layer with 32 groups.
    """
    return nn.GroupNorm(num_groups=32, num_channels=in_channels, eps=1e-6, affine=True)
    

@torch.jit.script
def swish(x: Tensor) -> Tensor:
    """
    Applies the Swish activation function: x * sigmoid(x).

    Args:
        x (Tensor): Input tensor.

    Returns:
        Tensor: Output tensor after applying the Swish activation.
    """
    return x * torch.sigmoid(x)


class VectorQuantizer(nn.Module):
    """
    Vector Quantizer for VQ-VAE.

    Args:
        codebook_size (int): Number of embedding vectors in the codebook.
        emb_dim (int): Dimensionality of each embedding vector.
        beta (float): Commitment cost factor for the VQ-VAE loss.
    """

    def __init__(self, codebook_size: int, emb_dim: int, beta: float) -> None:
        super(VectorQuantizer, self).__init__()
        self.codebook_size = codebook_size  # number of embeddings
        self.emb_dim = emb_dim  # dimension of embedding
        self.beta = beta  # commitment cost used in loss term
        self.embedding = nn.Embedding(self.codebook_size, self.emb_dim)
        self.embedding.weight.data.uniform_(-1.0 / self.codebook_size, 1.0 / self.codebook_size)

    def forward(self, z: Tensor) -> Tuple[Tensor, Tensor, Dict[str, Tensor]]:
        """
        Forward pass for the vector quantizer.

        Args:
            z (Tensor): Input tensor of shape (batch, channels, height, width).

        Returns:
            Tuple[Tensor, Tensor, Dict[str, Tensor]]: Quantized tensor, VQ loss, and additional statistics.
        """
        # Reshape z -> (batch, height, width, channels) and flatten
        z = z.permute(0, 2, 3, 1).contiguous()
        z_flattened = z.view(-1, self.emb_dim)

        # Compute distances to embedding vectors
        distances = self._compute_distances(z_flattened)

        # Find closest encoding indices
        min_encoding_indices = torch.argmin(distances, dim=1).unsqueeze(1)
        min_encodings = torch.zeros(min_encoding_indices.shape[0], self.codebook_size, device=z.device)
        min_encodings.scatter_(1, min_encoding_indices, 1)

        # Quantize latent vectors
        z_q = self._quantize(min_encodings, z.shape)

        # Compute loss for VQ-VAE
        vq_loss = self._compute_vq_loss(z, z_q)

        # Compute perplexity for the codebook
        perplexity = self._compute_perplexity(min_encodings)

        # Reshape back to original input shape
        z_q = z_q.permute(0, 3, 1, 2).contiguous()

        return z_q, vq_loss, {
            "perplexity": perplexity,
            "min_encodings": min_encodings,
            "min_encoding_indices": min_encoding_indices,
            "mean_distance": torch.mean(distances)
        }

    def _compute_distances(self, z_flattened: Tensor) -> Tensor:
        """Compute the distance between the flattened input and embeddings."""
        return (
            (z_flattened ** 2).sum(dim=1, keepdim=True) +
            (self.embedding.weight ** 2).sum(1) -
            2 * torch.matmul(z_flattened, self.embedding.weight.t())
        )

    def _quantize(self, min_encodings: Tensor, z_shape: torch.Size) -> Tensor:
        """Quantize the input based on the nearest embedding vectors."""
        z_q = torch.matmul(min_encodings, self.embedding.weight).view(z_shape)
        return z_q

    def _compute_vq_loss(self, z: Tensor, z_q: Tensor) -> Tensor:
        """Compute the VQ-VAE loss with a commitment cost."""
        return torch.mean((z_q.detach() - z) ** 2) + self.beta * torch.mean((z_q - z.detach()) ** 2)

    def _compute_perplexity(self, min_encodings: Tensor) -> Tensor:
        """Compute the perplexity of the codebook usage."""
        e_mean = torch.mean(min_encodings, dim=0)
        return torch.exp(-torch.sum(e_mean * torch.log(e_mean + 1e-10)))

    def get_codebook_feat(self, indices: Tensor, shape: Optional[torch.Size] = None) -> Tensor:
        """
        Retrieve the embedding vectors corresponding to the given indices.

        Args:
            indices (Tensor): Indices of the embedding vectors (shape: batch * token_num).
            shape (torch.Size, optional): The desired output shape.

        Returns:
            Tensor: The quantized latent vectors based on the provided indices.
        """
        indices = indices.view(-1, 1)
        min_encodings = torch.zeros(indices.shape[0], self.codebook_size, device=indices.device)
        min_encodings.scatter_(1, indices, 1)

        # Retrieve the quantized latent vectors
        z_q = torch.matmul(min_encodings.float(), self.embedding.weight)

        # Reshape to match the original input shape if specified
        if shape is not None:
            z_q = z_q.view(shape).permute(0, 3, 1, 2).contiguous()

        return z_q


class GumbelQuantizer(nn.Module):
    """
    Gumbel-Softmax-based quantizer.

    Args:
        codebook_size (int): Number of embeddings in the codebook.
        emb_dim (int): Dimensionality of each embedding vector.
        num_hiddens (int): Number of hidden channels from the encoder.
        straight_through (bool, optional): Whether to use the straight-through estimator during training. Default is False.
        kl_weight (float, optional): Weight for the KL divergence loss term. Default is 5e-4.
        temp_init (float, optional): Initial temperature for Gumbel-Softmax. Default is 1.0.
    """

    def __init__(
        self, 
        codebook_size: int, 
        emb_dim: int, 
        num_hiddens: int, 
        straight_through: bool = False, 
        kl_weight: float = 5e-4, 
        temp_init: float = 1.0
    ) -> None:
        super().__init__()
        self.codebook_size = codebook_size  # number of embeddings
        self.emb_dim = emb_dim  # dimension of embedding
        self.straight_through = straight_through
        self.temperature = temp_init
        self.kl_weight = kl_weight

        # Projection from the last encoder layer to logits for quantization
        self.proj = nn.Conv2d(num_hiddens, codebook_size, kernel_size=1)

        # Embedding lookup table
        self.embed = nn.Embedding(codebook_size, emb_dim)

    def forward(self, z: Tensor) -> Tuple[Tensor, Tensor, Dict[str, Tensor]]:
        """
        Forward pass for the Gumbel-Softmax quantizer.

        Args:
            z (Tensor): Input tensor from the encoder of shape (batch_size, num_hiddens, height, width).

        Returns:
            Tuple[Tensor, Tensor, Dict[str, Tensor]]: Quantized tensor, KL divergence loss, and additional statistics.
        """
        hard = self.straight_through if self.training else True

        # Project to logits for Gumbel-Softmax
        logits = self.proj(z)

        # Gumbel-Softmax operation
        soft_one_hot = F.gumbel_softmax(logits, tau=self.temperature, dim=1, hard=hard)

        # Quantize latent vectors using embedding lookup
        z_q = torch.einsum("b n h w, n d -> b d h w", soft_one_hot, self.embed.weight)

        # KL divergence loss
        kl_loss = self._compute_kl_loss(logits)

        # Get the indices of the minimum encodings
        min_encoding_indices = soft_one_hot.argmax(dim=1)

        return z_q, kl_loss, {
            "min_encoding_indices": min_encoding_indices
        }

    def _compute_kl_loss(self, logits: Tensor) -> Tensor:
        """
        Compute KL divergence loss for the quantizer.

        Args:
            logits (Tensor): Logits output by the projection layer.

        Returns:
            Tensor: The KL divergence loss term.
        """
        qy = F.softmax(logits, dim=1)
        kl_loss = self.kl_weight * torch.sum(qy * torch.log(qy * self.codebook_size + 1e-10), dim=1).mean()
        return kl_loss


class Downsample(nn.Module):
    """
    Downsamples the input tensor by a factor of 2 using a convolution with stride 2.

    Args:
        in_channels (int): Number of input channels.
    """
    
    def __init__(self, in_channels: int) -> None:
        super().__init__()
        self.conv = nn.Conv2d(in_channels, in_channels, kernel_size=3, stride=2, padding=0)

    def forward(self, x: Tensor) -> Tensor:
        """
        Forward pass for downsampling.

        Args:
            x (Tensor): Input tensor of shape (batch_size, channels, height, width).

        Returns:
            Tensor: Downsampled tensor.
        """
        # Pad the input to ensure proper downsampling with the Conv2d layer
        pad = (0, 1, 0, 1)  # pad right and bottom
        x = F.pad(x, pad, mode="constant", value=0)
        return self.conv(x)


class Upsample(nn.Module):
    """
    Upsamples the input tensor by a factor of 2 using nearest neighbor interpolation followed by a convolution.

    Args:
        in_channels (int): Number of input channels.
    """

    def __init__(self, in_channels: int) -> None:
        super().__init__()
        self.conv = nn.Conv2d(in_channels, in_channels, kernel_size=3, stride=1, padding=1)

    def forward(self, x: Tensor) -> Tensor:
        """
        Forward pass for upsampling.

        Args:
            x (Tensor): Input tensor of shape (batch_size, channels, height, width).

        Returns:
            Tensor: Upsampled tensor.
        """
        # Perform nearest-neighbor upsampling
        x = F.interpolate(x, scale_factor=2.0, mode="nearest")
        return self.conv(x)


class ResBlock(nn.Module):
    """
    A residual block consisting of two convolutional layers with normalization and activation,
    with an optional projection layer if the input and output channels are different.

    Args:
        in_channels (int): Number of input channels.
        out_channels (int, optional): Number of output channels. If None, it defaults to in_channels.
    """

    def __init__(self, in_channels: int, out_channels: int = None) -> None:
        super(ResBlock, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels if out_channels is not None else in_channels

        # First normalization and convolution
        self.norm1 = normalize(in_channels)
        self.conv1 = nn.Conv2d(in_channels, self.out_channels, kernel_size=3, stride=1, padding=1)

        # Second normalization and convolution
        self.norm2 = normalize(self.out_channels)
        self.conv2 = nn.Conv2d(self.out_channels, self.out_channels, kernel_size=3, stride=1, padding=1)

        # Optional projection layer if in_channels != out_channels
        self.conv_out = None
        if self.in_channels != self.out_channels:
            self.conv_out = nn.Conv2d(in_channels, self.out_channels, kernel_size=1, stride=1, padding=0)

    def forward(self, x_in: Tensor) -> Tensor:
        """
        Forward pass for the residual block.

        Args:
            x_in (Tensor): Input tensor of shape (batch_size, in_channels, height, width).

        Returns:
            Tensor: Output tensor after applying the residual block.
        """
        # First layer: normalization, activation (Swish), convolution
        x = self.norm1(x_in)
        x = swish(x)
        x = self.conv1(x)

        # Second layer: normalization, activation (Swish), convolution
        x = self.norm2(x)
        x = swish(x)
        x = self.conv2(x)

        # If in_channels != out_channels, apply the projection to x_in
        if self.in_channels != self.out_channels and self.conv_out is not None:
            x_in = self.conv_out(x_in)

        # Return the residual connection
        return x + x_in


class AttnBlock(nn.Module):
    """
    Self-Attention Block.

    This block applies self-attention to the input tensor and outputs a residual connection
    with the original input tensor.

    Args:
        in_channels (int): Number of input channels.
    """

    def __init__(self, in_channels: int) -> None:
        super().__init__()
        self.in_channels = in_channels

        # Normalization layer
        self.norm = normalize(in_channels)

        # Query, Key, and Value projection layers
        self.q = nn.Conv2d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        self.k = nn.Conv2d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)
        self.v = nn.Conv2d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)

        # Output projection layer
        self.proj_out = nn.Conv2d(in_channels, in_channels, kernel_size=1, stride=1, padding=0)

    def forward(self, x: Tensor) -> Tensor:
        """
        Forward pass for the self-attention block.

        Args:
            x (Tensor): Input tensor of shape (batch_size, in_channels, height, width).

        Returns:
            Tensor: Output tensor with the same shape as input, after applying self-attention and residual connection.
        """
        h_ = self.norm(x)
        q = self.q(h_)
        k = self.k(h_)
        v = self.v(h_)

        # Compute attention weights
        w_ = self._compute_attention(q, k)

        # Apply attention to values
        h_ = self._apply_attention(v, w_, q.shape)

        # Output projection and residual connection
        h_ = self.proj_out(h_)

        return x + h_

    def _compute_attention(self, q: Tensor, k: Tensor) -> Tensor:
        """
        Compute the attention weights.

        Args:
            q (Tensor): Query tensor of shape (batch_size, in_channels, height * width).
            k (Tensor): Key tensor of shape (batch_size, in_channels, height * width).

        Returns:
            Tensor: Attention weights of shape (batch_size, height * width, height * width).
        """
        b, c, h, w = q.shape
        q = q.reshape(b, c, h * w).permute(0, 2, 1)
        k = k.reshape(b, c, h * w)
        w_ = torch.bmm(q, k)
        w_ = w_ * (c ** -0.5)
        return F.softmax(w_, dim=2)

    def _apply_attention(self, v: Tensor, w_: Tensor, q_shape: torch.Size) -> Tensor:
        """
        Apply the computed attention weights to the value tensor.

        Args:
            v (Tensor): Value tensor of shape (batch_size, in_channels, height * width).
            w_ (Tensor): Attention weights.
            q_shape (torch.Size): Shape of the query tensor.

        Returns:
            Tensor: Output tensor after applying attention.
        """
        b, c, h, w = q_shape
        v = v.reshape(b, c, h * w)
        w_ = w_.permute(0, 2, 1)
        h_ = torch.bmm(v, w_)
        return h_.reshape(b, c, h, w)


class Encoder(nn.Module):
    """
    Encoder class that processes input images through a series of residual, attention, and downsampling blocks.

    Args:
        in_channels (int): Number of input channels (e.g., 3 for RGB images).
        nf (int): Number of feature maps.
        emb_dim (int): Dimensionality of the latent embeddings.
        ch_mult (List[int]): Channel multiplier for each resolution level.
        num_res_blocks (int): Number of residual blocks at each resolution.
        resolution (int): Initial resolution of the input images (height/width).
        attn_resolutions (List[int]): Resolutions at which attention is applied.
    """

    def __init__(
        self,
        in_channels: int,
        nf: int,
        emb_dim: int,
        ch_mult: List[int],
        num_res_blocks: int,
        resolution: int,
        attn_resolutions: List[int]
    ) -> None:
        super().__init__()

        self.nf = nf
        self.num_resolutions = len(ch_mult)
        self.num_res_blocks = num_res_blocks
        self.resolution = resolution
        self.attn_resolutions = attn_resolutions

        curr_res = self.resolution
        in_ch_mult = (1,) + tuple(ch_mult)

        blocks = []

        # Initial convolution block
        blocks.append(nn.Conv2d(in_channels, nf, kernel_size=3, stride=1, padding=1))

        # Residual and downsampling blocks with attention
        for i in range(self.num_resolutions):
            block_in_ch = nf * in_ch_mult[i]
            block_out_ch = nf * ch_mult[i]
            blocks += self._make_res_blocks(block_in_ch, block_out_ch, curr_res)
            block_in_ch = block_out_ch
            if i != self.num_resolutions - 1:
                blocks.append(Downsample(block_in_ch))
                curr_res //= 2

        # Final residual and attention blocks
        blocks.append(ResBlock(block_in_ch, block_in_ch))
        blocks.append(AttnBlock(block_in_ch))
        blocks.append(ResBlock(block_in_ch, block_in_ch))

        # Normalization and projection to embedding dimension
        blocks.append(normalize(block_in_ch))
        blocks.append(nn.Conv2d(block_in_ch, emb_dim, kernel_size=3, stride=1, padding=1))

        self.blocks = nn.ModuleList(blocks)

    def _make_res_blocks(self, block_in_ch: int, block_out_ch: int, curr_res: int) -> List[nn.Module]:
        """
        Creates a list of residual and attention blocks for a given resolution.

        Args:
            block_in_ch (int): Number of input channels for the residual block.
            block_out_ch (int): Number of output channels for the residual block.
            curr_res (int): Current resolution of the feature map.

        Returns:
            List[nn.Module]: List of residual and attention blocks.
        """
        blocks = []
        for _ in range(self.num_res_blocks):
            blocks.append(ResBlock(block_in_ch, block_out_ch))
            block_in_ch = block_out_ch
            if curr_res in self.attn_resolutions:
                blocks.append(AttnBlock(block_in_ch))
        return blocks

    def forward(self, x: Tensor) -> Tensor:
        """
        Forward pass through the encoder.

        Args:
            x (Tensor): Input tensor of shape (batch_size, in_channels, height, width).

        Returns:
            Tensor: Output tensor after processing through the encoder.
        """
        for block in self.blocks:
            x = block(x)
        return x


class Generator(nn.Module):
    """
    A generator network that upsamples and transforms an input tensor into an image using residual, attention, and upsampling blocks.

    Args:
        nf (int): Number of base feature maps.
        emb_dim (int): Dimensionality of the input embedding.
        ch_mult (List[int]): Channel multipliers for each resolution level.
        res_blocks (int): Number of residual blocks at each resolution level.
        img_size (int): Resolution of the output image.
        attn_resolutions (List[int]): Resolutions at which attention blocks are applied.
    """

    def __init__(
        self,
        nf: int,
        emb_dim: int,
        ch_mult: List[int],
        res_blocks: int,
        img_size: int,
        attn_resolutions: List[int]
    ) -> None:
        super().__init__()
        self.nf = nf
        self.ch_mult = ch_mult
        self.num_resolutions = len(ch_mult)
        self.num_res_blocks = res_blocks
        self.resolution = img_size
        self.attn_resolutions = attn_resolutions
        self.in_channels = emb_dim
        self.out_channels = 3

        curr_res = self.resolution // (2 ** (self.num_resolutions - 1))
        block_in_ch = nf * ch_mult[-1]

        blocks = []

        # Initial convolution block
        blocks.append(nn.Conv2d(self.in_channels, block_in_ch, kernel_size=3, stride=1, padding=1))

        # Initial residual and attention blocks
        blocks += self._add_initial_res_attention_blocks(block_in_ch)

        # Residual, attention, and upsampling blocks
        blocks += self._build_upsample_blocks(curr_res, block_in_ch)

        # Final normalization and convolution
        blocks.append(normalize(block_in_ch))
        blocks.append(nn.Conv2d(block_in_ch, self.out_channels, kernel_size=3, stride=1, padding=1))

        self.blocks = nn.ModuleList(blocks)

    def _add_initial_res_attention_blocks(self, block_in_ch: int) -> List[nn.Module]:
        """
        Adds the initial residual and attention blocks at the highest resolution.

        Args:
            block_in_ch (int): Number of input channels for the residual block.

        Returns:
            List[nn.Module]: List of initial residual and attention blocks.
        """
        blocks = [
            ResBlock(block_in_ch, block_in_ch),
            AttnBlock(block_in_ch),
            ResBlock(block_in_ch, block_in_ch)
        ]
        return blocks

    def _build_upsample_blocks(self, curr_res: int, block_in_ch: int) -> List[nn.Module]:
        """
        Build the upsampling blocks with residual and attention layers.

        Args:
            curr_res (int): Current resolution of the feature map.
            block_in_ch (int): Number of input channels for the residual block.

        Returns:
            List[nn.Module]: List of residual, attention, and upsampling blocks.
        """
        blocks = []
        for i in reversed(range(self.num_resolutions)):
            block_out_ch = self.nf * self.ch_mult[i]

            for _ in range(self.num_res_blocks):
                blocks.append(ResBlock(block_in_ch, block_out_ch))
                block_in_ch = block_out_ch

                if curr_res in self.attn_resolutions:
                    blocks.append(AttnBlock(block_in_ch))

            if i != 0:
                blocks.append(Upsample(block_in_ch))
                curr_res *= 2

        return blocks

    def forward(self, x: Tensor) -> Tensor:
        """
        Forward pass for the generator.

        Args:
            x (Tensor): Input tensor of shape (batch_size, emb_dim, height, width).

        Returns:
            Tensor: Output tensor after processing through the generator, typically an image of shape (batch_size, 3, height, width).
        """
        for block in self.blocks:
            x = block(x)
        return x

  
@ARCH_REGISTRY.register()
class VQAutoEncoder(nn.Module):
    """
    Vector Quantized Autoencoder (VQ-VAE) class with support for both nearest-neighbor and Gumbel-Softmax quantization.

    Args:
        img_size (int): Input image size (height and width).
        nf (int): Number of base feature maps.
        ch_mult (List[int]): Channel multipliers for each resolution level.
        quantizer (str, optional): Type of quantizer to use ('nearest' or 'gumbel'). Default is 'nearest'.
        res_blocks (int, optional): Number of residual blocks at each resolution level. Default is 2.
        attn_resolutions (List[int], optional): Resolutions at which attention blocks are applied. Default is [16].
        codebook_size (int, optional): Number of entries in the codebook. Default is 1024.
        emb_dim (int, optional): Dimensionality of the embedding vectors. Default is 256.
        beta (float, optional): Beta parameter for the VQ loss in nearest quantizer. Default is 0.25.
        gumbel_straight_through (bool, optional): Whether to use straight-through estimator for Gumbel quantizer. Default is False.
        gumbel_kl_weight (float, optional): KL divergence weight for Gumbel quantizer. Default is 1e-8.
        model_path (str, optional): Path to the pre-trained model to load. Default is None.
    """

    def __init__(
        self,
        img_size: int,
        nf: int,
        ch_mult: List[int],
        quantizer: str = "nearest",
        res_blocks: int = 2,
        attn_resolutions: List[int] = [16],
        codebook_size: int = 1024,
        emb_dim: int = 256,
        beta: float = 0.25,
        gumbel_straight_through: bool = False,
        gumbel_kl_weight: float = 1e-8,
        model_path: Optional[str] = None
    ) -> None:
        super().__init__()
        logger = get_root_logger()

        # Encoder and generator settings
        self.in_channels = 3
        self.nf = nf
        self.n_blocks = res_blocks
        self.codebook_size = codebook_size
        self.embed_dim = emb_dim
        self.ch_mult = ch_mult
        self.resolution = img_size
        self.attn_resolutions = attn_resolutions
        self.quantizer_type = quantizer

        # Initialize encoder
        self.encoder = Encoder(
            self.in_channels, self.nf, self.embed_dim, self.ch_mult,
            self.n_blocks, self.resolution, self.attn_resolutions
        )

        # Initialize quantizer (nearest or Gumbel)
        self._initialize_quantizer(
            quantizer, beta, emb_dim, codebook_size, gumbel_straight_through, gumbel_kl_weight
        )

        # Initialize generator
        self.generator = Generator(
            self.nf, self.embed_dim, self.ch_mult, self.n_blocks, self.resolution, self.attn_resolutions
        )

        # Load pre-trained model if specified
        if model_path is not None:
            self._load_pretrained_model(model_path, logger)

    def _initialize_quantizer(
        self,
        quantizer: str,
        beta: float,
        emb_dim: int,
        codebook_size: int,
        gumbel_straight_through: bool,
        gumbel_kl_weight: float
    ) -> None:
        """
        Initialize the quantizer (either 'nearest' or 'gumbel').

        Args:
            quantizer (str): Type of quantizer ('nearest' or 'gumbel').
            beta (float): Beta value for nearest quantizer.
            emb_dim (int): Embedding dimension.
            codebook_size (int): Size of the codebook.
            gumbel_straight_through (bool): Whether to use straight-through for Gumbel quantizer.
            gumbel_kl_weight (float): KL weight for Gumbel quantizer.
        """
        if quantizer == "nearest":
            self.beta = beta
            self.quantize = VectorQuantizer(codebook_size, emb_dim, beta)
        elif quantizer == "gumbel":
            self.gumbel_num_hiddens = emb_dim
            self.straight_through = gumbel_straight_through
            self.kl_weight = gumbel_kl_weight
            self.quantize = GumbelQuantizer(
                codebook_size, emb_dim, self.gumbel_num_hiddens, self.straight_through, self.kl_weight
            )

    def _load_pretrained_model(self, model_path: str, logger) -> None:
        """
        Load a pre-trained model from the specified path.

        Args:
            model_path (str): Path to the pre-trained model.
            logger: Logger object to log the loading process.
        """
        chkpt = torch.load(model_path, map_location="cpu")
        if "params_ema" in chkpt:
            self.load_state_dict(chkpt["params_ema"])
            logger.info(f'Model loaded from: {model_path} [params_ema]')
        elif "params" in chkpt:
            self.load_state_dict(chkpt["params"])
            logger.info(f'Model loaded from: {model_path} [params]')
        else:
            raise ValueError(f"Invalid checkpoint format in {model_path}")

    def forward(self, x: Tensor) -> Tuple[Tensor, Tensor, dict]:
        """
        Forward pass of the VQ-VAE.

        Args:
            x (Tensor): Input tensor of shape (batch_size, in_channels, height, width).

        Returns:
            Tuple[Tensor, Tensor, dict]: Generated image, codebook loss, and quantization stats.
        """
        x = self.encoder(x)
        quant, codebook_loss, quant_stats = self.quantize(x)
        x = self.generator(quant)
        return x, codebook_loss, quant_stats


@ARCH_REGISTRY.register()
class VQGANDiscriminator(nn.Module):
    """
    Patch-based Discriminator for VQ-GAN.

    Args:
        nc (int, optional): Number of input channels. Default is 3 (e.g., for RGB images).
        ndf (int, optional): Number of filters in the first convolutional layer. Default is 64.
        n_layers (int, optional): Number of layers in the discriminator. Default is 4.
        model_path (str, optional): Path to a pre-trained model. Default is None.
    """

    def __init__(
        self, 
        nc: int = 3, 
        ndf: int = 64, 
        n_layers: int = 4, 
        model_path: Optional[str] = None
    ) -> None:
        super().__init__()

        # Build the layers
        self.main = self._build_layers(nc, ndf, n_layers)

        # Load the pre-trained model if provided
        if model_path is not None:
            self._load_pretrained_model(model_path)

    def _build_layers(self, nc: int, ndf: int, n_layers: int) -> nn.Sequential:
        """
        Build the layers of the discriminator.

        Args:
            nc (int): Number of input channels.
            ndf (int): Number of filters in the first convolutional layer.
            n_layers (int): Number of layers in the discriminator.

        Returns:
            nn.Sequential: The discriminator's main layers.
        """
        layers = [
            nn.Conv2d(nc, ndf, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.2, inplace=True)
        ]

        ndf_mult = 1
        for n in range(1, n_layers):
            ndf_mult_prev = ndf_mult
            ndf_mult = min(2 ** n, 8)
            layers += [
                nn.Conv2d(ndf * ndf_mult_prev, ndf * ndf_mult, kernel_size=4, stride=2, padding=1, bias=False),
                nn.BatchNorm2d(ndf * ndf_mult),
                nn.LeakyReLU(0.2, inplace=True)
            ]

        # Final layers after all resolutions
        ndf_mult_prev = ndf_mult
        ndf_mult = min(2 ** n_layers, 8)
        layers += [
            nn.Conv2d(ndf * ndf_mult_prev, ndf * ndf_mult, kernel_size=4, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(ndf * ndf_mult),
            nn.LeakyReLU(0.2, inplace=True)
        ]
        layers += [
            nn.Conv2d(ndf * ndf_mult, 1, kernel_size=4, stride=1, padding=1)  # Output 1 channel prediction map
        ]

        return nn.Sequential(*layers)

    def _load_pretrained_model(self, model_path: str) -> None:
        """
        Load a pre-trained model from the specified path.

        Args:
            model_path (str): Path to the pre-trained model.
        """
        chkpt = torch.load(model_path, map_location="cpu")
        if "params_d" in chkpt:
            self.load_state_dict(chkpt["params_d"])
        elif "params" in chkpt:
            self.load_state_dict(chkpt["params"])
        else:
            raise ValueError(f"Invalid checkpoint format in {model_path}")

    def forward(self, x: Tensor) -> Tensor:
        """
        Forward pass of the discriminator.

        Args:
            x (Tensor): Input tensor of shape (batch_size, channels, height, width).

        Returns:
            Tensor: Output prediction map from the discriminator.
        """
        return self.main(x)
