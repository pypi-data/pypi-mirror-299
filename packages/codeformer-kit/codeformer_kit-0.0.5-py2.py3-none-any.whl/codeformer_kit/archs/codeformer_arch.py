import math
import torch
from torch import nn, Tensor
import torch.nn.functional as F
from typing import Optional, List, Tuple, Callable

from codeformer_kit.archs.vqgan_arch import ResBlock, VQAutoEncoder
from codeformer_kit.utils.registry import ARCH_REGISTRY


def calc_mean_std(feat: Tensor, eps: float = 1e-5) -> Tuple[Tensor, Tensor]:
    """
    Calculate the mean and standard deviation for adaptive instance normalization (AdaIN).

    Args:
        feat (Tensor): Input 4D tensor of shape (batch_size, channels, height, width).
        eps (float, optional): A small value added to the variance to avoid divide-by-zero. Default is 1e-5.

    Returns:
        Tuple[Tensor, Tensor]: The mean and standard deviation of the input tensor.
            Both returned tensors have the shape (batch_size, channels, 1, 1).
    """
    assert feat.dim() == 4, 'Input feature should be a 4D tensor.'
    
    # Extract batch size and channel size
    b, c = feat.size(0), feat.size(1)
    
    # Compute variance and add epsilon for numerical stability
    feat_var = feat.view(b, c, -1).var(dim=2, unbiased=False) + eps
    feat_std = feat_var.sqrt().view(b, c, 1, 1)
    
    # Compute mean
    feat_mean = feat.view(b, c, -1).mean(dim=2).view(b, c, 1, 1)
    
    return feat_mean, feat_std


def adaptive_instance_normalization(content_feat: Tensor, style_feat: Tensor) -> Tensor:
    """
    Apply adaptive instance normalization (AdaIN) to adjust the content features to have the 
    same color and illumination statistics (mean and standard deviation) as the style features.

    Args:
        content_feat (Tensor): The content feature tensor of shape (batch_size, channels, height, width).
        style_feat (Tensor): The style feature tensor of shape (batch_size, channels, height, width).

    Returns:
        Tensor: The normalized feature tensor with the same statistics as the style features.
    """
    size = content_feat.size()

    # Calculate mean and std for style and content features
    style_mean, style_std = calc_mean_std(style_feat)
    content_mean, content_std = calc_mean_std(content_feat)

    # Normalize the content feature
    normalized_feat = (content_feat - content_mean.expand(size)) / content_std.expand(size)

    # Scale by the style statistics and return the final feature
    return normalized_feat * style_std.expand(size) + style_mean.expand(size)


class PositionEmbeddingSine(nn.Module):
    """
    A standard version of position embedding, similar to the one used in the "Attention is All You Need" paper,
    generalized to work on images.

    Args:
        num_pos_feats (int, optional): Number of positional features. Default is 64.
        temperature (int, optional): Temperature parameter for scaling. Default is 10000.
        normalize (bool, optional): Whether to normalize the position embeddings. Default is False.
        scale (float, optional): Scale factor for the embeddings. Required if `normalize` is True. Default is None.
    """

    def __init__(
        self, 
        num_pos_feats: int = 64, 
        temperature: int = 10000, 
        normalize: bool = False, 
        scale: Optional[float] = None
    ) -> None:
        super().__init__()
        self.num_pos_feats = num_pos_feats
        self.temperature = temperature
        self.normalize = normalize
        
        if scale is not None and not normalize:
            raise ValueError("normalize should be True if scale is passed")
        self.scale = scale if scale is not None else 2 * math.pi

    def forward(self, x: Tensor, mask: Optional[Tensor] = None) -> Tensor:
        """
        Forward pass to compute position embeddings.

        Args:
            x (Tensor): Input tensor of shape (batch_size, channels, height, width).
            mask (Tensor, optional): Binary mask tensor of shape (batch_size, height, width). Default is None.

        Returns:
            Tensor: Position embeddings of shape (batch_size, num_pos_feats*2, height, width).
        """
        mask = self._prepare_mask(x, mask)
        not_mask = ~mask

        # Create positional encodings for x and y dimensions
        y_embed, x_embed = self._get_position_embeddings(not_mask)

        if self.normalize:
            x_embed, y_embed = self._normalize_embeddings(x_embed, y_embed)

        # Compute sine and cosine embeddings
        pos = self._compute_sine_cosine_embeddings(x_embed, y_embed, x.device)

        return pos

    def _prepare_mask(self, x: Tensor, mask: Optional[Tensor]) -> Tensor:
        """Prepare the binary mask if not provided."""
        if mask is None:
            mask = torch.zeros((x.size(0), x.size(2), x.size(3)), device=x.device, dtype=torch.bool)
        return mask

    def _get_position_embeddings(self, not_mask: Tensor) -> Tuple[Tensor, Tensor]:
        """Calculate cumulative sums for x and y positional embeddings."""
        y_embed = not_mask.cumsum(1, dtype=torch.float32)
        x_embed = not_mask.cumsum(2, dtype=torch.float32)
        return y_embed, x_embed

    def _normalize_embeddings(self, x_embed: Tensor, y_embed: Tensor) -> Tuple[Tensor, Tensor]:
        """Normalize positional embeddings if required."""
        eps = 1e-6
        y_embed = y_embed / (y_embed[:, -1:, :] + eps) * self.scale
        x_embed = x_embed / (x_embed[:, :, -1:] + eps) * self.scale
        return x_embed, y_embed

    def _compute_sine_cosine_embeddings(self, x_embed: Tensor, y_embed: Tensor, device: torch.device) -> Tensor:
        """Compute sine and cosine embeddings from the positional encodings."""
        dim_t = torch.arange(self.num_pos_feats, dtype=torch.float32, device=device)
        dim_t = self.temperature ** (2 * (dim_t // 2) / self.num_pos_feats)

        # Compute sine and cosine embeddings for x and y dimensions
        pos_x = x_embed[:, :, :, None] / dim_t
        pos_y = y_embed[:, :, :, None] / dim_t
        pos_x = torch.stack((pos_x[:, :, :, 0::2].sin(), pos_x[:, :, :, 1::2].cos()), dim=4).flatten(3)
        pos_y = torch.stack((pos_y[:, :, :, 0::2].sin(), pos_y[:, :, :, 1::2].cos()), dim=4).flatten(3)

        # Concatenate and reshape the position embeddings
        pos = torch.cat((pos_y, pos_x), dim=3).permute(0, 3, 1, 2)
        return pos


def _get_activation_fn(activation: str) -> Callable:
    """
    Return the activation function corresponding to the given string.

    Args:
        activation (str): The name of the activation function ('relu', 'gelu', 'glu').

    Returns:
        Callable: The corresponding activation function from torch.nn.functional.

    Raises:
        ValueError: If the activation string is not one of 'relu', 'gelu', or 'glu'.
    """
    activation_functions = {
        "relu": F.relu,
        "gelu": F.gelu,
        "glu": F.glu
    }

    if activation in activation_functions:
        return activation_functions[activation]
    
    raise ValueError(f"Invalid activation function: {activation}. Supported: relu, gelu, glu.")


class TransformerSALayer(nn.Module):
    """
    Self-Attention Layer for Transformer.

    Args:
        embed_dim (int): The embedding dimension of the input.
        nhead (int, optional): Number of attention heads. Default is 8.
        dim_mlp (int, optional): The dimensionality of the feedforward layer (MLP). Default is 2048.
        dropout (float, optional): Dropout rate. Default is 0.0.
        activation (str, optional): Activation function ('relu', 'gelu', 'glu'). Default is 'gelu'.
    """

    def __init__(
        self, 
        embed_dim: int, 
        nhead: int = 8, 
        dim_mlp: int = 2048, 
        dropout: float = 0.0, 
        activation: str = "gelu"
    ) -> None:
        super().__init__()

        # Self-attention mechanism
        self.self_attn = nn.MultiheadAttention(embed_dim, nhead, dropout=dropout)

        # Feedforward network (MLP)
        self.linear1 = nn.Linear(embed_dim, dim_mlp)
        self.dropout = nn.Dropout(dropout)
        self.linear2 = nn.Linear(dim_mlp, embed_dim)

        # Layer normalization and dropout
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)

        # Activation function
        self.activation = _get_activation_fn(activation)

    def with_pos_embed(self, tensor: Tensor, pos: Optional[Tensor]) -> Tensor:
        """
        Add positional embeddings to the input tensor if available.

        Args:
            tensor (Tensor): The input tensor.
            pos (Tensor, optional): The positional embeddings.

        Returns:
            Tensor: Tensor with positional embeddings added (if provided).
        """
        return tensor if pos is None else tensor + pos

    def forward(
        self, 
        tgt: Tensor,
        tgt_mask: Optional[Tensor] = None,
        tgt_key_padding_mask: Optional[Tensor] = None,
        query_pos: Optional[Tensor] = None
    ) -> Tensor:
        """
        Forward pass of the Transformer self-attention layer.

        Args:
            tgt (Tensor): The target sequence tensor of shape (seq_len, batch_size, embed_dim).
            tgt_mask (Tensor, optional): The mask for the target sequence. Default is None.
            tgt_key_padding_mask (Tensor, optional): The mask for padding positions. Default is None.
            query_pos (Tensor, optional): Positional encoding for the query. Default is None.

        Returns:
            Tensor: The output tensor after the self-attention and feedforward layers.
        """
        # Self-attention with normalization
        tgt2 = self.norm1(tgt)
        q = k = self.with_pos_embed(tgt2, query_pos)
        attn_output = self.self_attn(
            q, k, value=tgt2, attn_mask=tgt_mask, key_padding_mask=tgt_key_padding_mask
        )[0]
        tgt = tgt + self.dropout1(attn_output)

        # Feedforward network with normalization
        tgt2 = self.norm2(tgt)
        ffn_output = self.linear2(self.dropout(self.activation(self.linear1(tgt2))))
        tgt = tgt + self.dropout2(ffn_output)

        return tgt


class FuseSFTBlock(nn.Module):
    """
    A fusion block that combines encoded and decoded features using scale and shift transformations.

    Args:
        in_ch (int): Number of input channels.
        out_ch (int): Number of output channels.
    """

    def __init__(self, in_ch: int, out_ch: int) -> None:
        super().__init__()

        # Encoding block for the concatenated input features
        self.encode_enc = ResBlock(2 * in_ch, out_ch)

        # Scale branch: Applies a scaling factor to the decoded features
        self.scale = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, kernel_size=3, padding=1),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(out_ch, out_ch, kernel_size=3, padding=1)
        )

        # Shift branch: Applies a shift factor to the decoded features
        self.shift = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, kernel_size=3, padding=1),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(out_ch, out_ch, kernel_size=3, padding=1)
        )

    def forward(self, enc_feat: Tensor, dec_feat: Tensor, w: float = 1.0) -> Tensor:
        """
        Forward pass of the fusion block.

        Args:
            enc_feat (Tensor): The encoded features tensor.
            dec_feat (Tensor): The decoded features tensor.
            w (float, optional): The weight factor for scaling the residual. Default is 1.0.

        Returns:
            Tensor: The fused feature tensor.
        """
        # Concatenate encoder and decoder features and pass through the encode block
        enc_feat = self.encode_enc(torch.cat([enc_feat, dec_feat], dim=1))

        # Apply scale and shift transformations
        scale = self.scale(enc_feat)
        shift = self.shift(enc_feat)

        # Compute the residual and fuse it with the decoded features
        residual = w * (dec_feat * scale + shift)
        out = dec_feat + residual

        return out


@ARCH_REGISTRY.register()
class CodeFormer(VQAutoEncoder):
    """
    CodeFormer model for image processing, inheriting from VQAutoEncoder.

    Args:
        dim_embd (int, optional): Embedding dimension size. Default is 512.
        n_head (int, optional): Number of attention heads in the Transformer. Default is 8.
        n_layers (int, optional): Number of Transformer layers. Default is 9.
        codebook_size (int, optional): Size of the codebook for quantization. Default is 1024.
        latent_size (int, optional): Size of the latent space. Default is 256.
        connect_list (List[str], optional): List of layers to connect. Default is ['32', '64', '128', '256'].
        fix_modules (List[str], optional): Modules to fix and not update during training. Default is ['quantize', 'generator'].
        vqgan_path (str, optional): Path to the VQGAN pre-trained model. Default is None.
    """

    def __init__(
        self,
        dim_embd: int = 512,
        n_head: int = 8,
        n_layers: int = 9,
        codebook_size: int = 1024,
        latent_size: int = 256,
        connect_list: List[str] = ['32', '64', '128', '256'],
        fix_modules: List[str] = ['quantize', 'generator'],
        vqgan_path: Optional[str] = None
    ) -> None:
        super().__init__(512, 64, [1, 2, 2, 4, 4, 8], 'nearest', 2, [16], codebook_size)

        if vqgan_path is not None:
            self.load_state_dict(torch.load(vqgan_path, map_location='cpu')['params_ema'])

        if fix_modules:
            self._fix_modules(fix_modules)

        self.connect_list = connect_list
        self.n_layers = n_layers
        self.dim_embd = dim_embd
        self.dim_mlp = dim_embd * 2

        self.position_emb = nn.Parameter(torch.zeros(latent_size, self.dim_embd))
        self.feat_emb = nn.Linear(256, self.dim_embd)

        # Transformer layers
        self.ft_layers = nn.Sequential(
            *[TransformerSALayer(embed_dim=dim_embd, nhead=n_head, dim_mlp=self.dim_mlp, dropout=0.0) for _ in range(self.n_layers)]
        )

        # Prediction head
        self.idx_pred_layer = nn.Sequential(
            nn.LayerNorm(dim_embd),
            nn.Linear(dim_embd, codebook_size, bias=False)
        )

        self.channels = {'16': 512, '32': 256, '64': 256, '128': 128, '256': 128, '512': 64}
        self.fuse_encoder_block = {'512': 2, '256': 5, '128': 8, '64': 11, '32': 14, '16': 18}
        self.fuse_generator_block = {'16': 6, '32': 9, '64': 12, '128': 15, '256': 18, '512': 21}

        # Fusion layers
        self.fuse_convs_dict = nn.ModuleDict()
        for f_size in self.connect_list:
            in_ch = self.channels[f_size]
            self.fuse_convs_dict[f_size] = FuseSFTBlock(in_ch, in_ch)

    def _fix_modules(self, fix_modules: List[str]) -> None:
        """
        Freeze the parameters of specified modules to prevent them from updating during training.
        """
        for module in fix_modules:
            for param in getattr(self, module).parameters():
                param.requires_grad = False

    def _init_weights(self, module: nn.Module) -> None:
        """
        Initialize the weights of the module.
        """
        if isinstance(module, (nn.Linear, nn.Embedding)):
            module.weight.data.normal_(mean=0.0, std=0.02)
            if isinstance(module, nn.Linear) and module.bias is not None:
                module.bias.data.zero_()
        elif isinstance(module, nn.LayerNorm):
            module.bias.data.zero_()
            module.weight.data.fill_(1.0)

    def forward(
        self, 
        x: Tensor, 
        w: float = 0, 
        detach_16: bool = True, 
        code_only: bool = False, 
        adain: bool = False
    ) -> Tensor:
        """
        Forward pass of the CodeFormer model.

        Args:
            x (Tensor): Input tensor.
            w (float, optional): Weight for scaling the residual connections. Default is 0.
            detach_16 (bool, optional): Whether to detach quantized features at 16x16 resolution. Default is True.
            code_only (bool, optional): Whether to return only the logits and latent features (for training stage II). Default is False.
            adain (bool, optional): Whether to use adaptive instance normalization. Default is False.

        Returns:
            Tensor: Output tensor.
        """
        # Encoder
        enc_feat_dict = {}
        out_list = [self.fuse_encoder_block[f_size] for f_size in self.connect_list]
        for i, block in enumerate(self.encoder.blocks):
            x = block(x)
            if i in out_list:
                enc_feat_dict[str(x.shape[-1])] = x.clone()

        lq_feat = x

        # Transformer
        pos_emb = self.position_emb.unsqueeze(1).repeat(1, x.shape[0], 1)
        feat_emb = self.feat_emb(lq_feat.flatten(2).permute(2, 0, 1))
        query_emb = feat_emb

        for layer in self.ft_layers:
            query_emb = layer(query_emb, query_pos=pos_emb)

        logits = self.idx_pred_layer(query_emb).permute(1, 0, 2)

        if code_only:
            return logits, lq_feat

        # Quantization
        soft_one_hot = F.softmax(logits, dim=2)
        _, top_idx = torch.topk(soft_one_hot, 1, dim=2)
        quant_feat = self.quantize.get_codebook_feat(top_idx, shape=[x.shape[0], 16, 16, 256])

        if detach_16:
            quant_feat = quant_feat.detach()

        if adain:
            quant_feat = adaptive_instance_normalization(quant_feat, lq_feat)

        # Generator
        x = quant_feat
        fuse_list = [self.fuse_generator_block[f_size] for f_size in self.connect_list]

        for i, block in enumerate(self.generator.blocks):
            x = block(x)
            if i in fuse_list and w > 0:
                f_size = str(x.shape[-1])
                x = self.fuse_convs_dict[f_size](enc_feat_dict[f_size].detach(), x, w)

        return x, logits, lq_feat
