import collections.abc
import math
import torch
import torchvision
import warnings
from distutils.version import LooseVersion
from itertools import repeat
from torch import nn
from torch import Tensor
from torch.nn import functional as F
from torch.nn import init as init
from torch.nn.modules.batchnorm import _BatchNorm
from typing import List, Union, Callable, Any, Tuple

from codeformer_kit.ops.dcn import ModulatedDeformConvPack, modulated_deform_conv
from codeformer_kit.utils import get_root_logger


@torch.no_grad()
def default_init_weights(
    module_list: Union[List[nn.Module], nn.Module], 
    scale: float = 1.0, 
    bias_fill: float = 0.0, 
    **kwargs
) -> None:
    """Initialize network weights for convolutional, linear, and batch normalization layers.

    Args:
        module_list (list[nn.Module] | nn.Module): A list of modules or a single module to be initialized.
        scale (float): Scale factor for initialized weights, particularly for residual blocks. Default: 1.0.
        bias_fill (float): The value to fill bias tensors. Default: 0.0.
        kwargs (dict): Additional arguments for initialization functions.
    """
    if not isinstance(module_list, list):
        module_list = [module_list]  # Ensure module_list is a list

    for module in module_list:
        for m in module.modules():
            if isinstance(m, nn.Conv2d):
                _init_conv2d(m, scale, bias_fill, **kwargs)
            elif isinstance(m, nn.Linear):
                _init_linear(m, scale, bias_fill, **kwargs)
            elif isinstance(m, _BatchNorm):
                _init_batchnorm(m, bias_fill)


def _init_conv2d(m: nn.Conv2d, scale: float, bias_fill: float, **kwargs) -> None:
    """Helper function to initialize Conv2D layers."""
    init.kaiming_normal_(m.weight, **kwargs)
    m.weight.data *= scale
    if m.bias is not None:
        m.bias.data.fill_(bias_fill)


def _init_linear(m: nn.Linear, scale: float, bias_fill: float, **kwargs) -> None:
    """Helper function to initialize Linear layers."""
    init.kaiming_normal_(m.weight, **kwargs)
    m.weight.data *= scale
    if m.bias is not None:
        m.bias.data.fill_(bias_fill)


def _init_batchnorm(m: _BatchNorm, bias_fill: float) -> None:
    """Helper function to initialize BatchNorm layers."""
    init.constant_(m.weight, 1)
    if m.bias is not None:
        m.bias.data.fill_(bias_fill)


def make_layer(basic_block: nn.Module, num_basic_blocks: int, **kwargs) -> nn.Sequential:
    """
    Create a sequential container by stacking the specified number of basic blocks.

    Args:
        basic_block (nn.Module): The block class to be repeated. Should be a subclass of nn.Module.
        num_basic_blocks (int): The number of blocks to stack sequentially.
        **kwargs: Additional keyword arguments to pass to each block during instantiation.

    Returns:
        nn.Sequential: A sequential container of the stacked blocks.
    """
    return nn.Sequential(*(basic_block(**kwargs) for _ in range(num_basic_blocks)))


class ResidualBlockNoBN(nn.Module):
    """
    Residual block without batch normalization (BN).

    Structure:
        --- Conv -> ReLU -> Conv --+-
         |                         |
         +-------------------------+

    Args:
        num_feat (int, optional): Number of channels for the intermediate features. Default is 64.
        res_scale (float, optional): Scaling factor for the residual connection. Default is 1.
        pytorch_init (bool, optional): Whether to use PyTorch's default weight initialization.
            If False, `default_init_weights` is used. Default is False.
    """

    def __init__(self, num_feat: int = 64, res_scale: float = 1.0, pytorch_init: bool = False) -> None:
        super().__init__()
        self.res_scale = res_scale
        self.conv1 = nn.Conv2d(num_feat, num_feat, kernel_size=3, stride=1, padding=1, bias=True)
        self.conv2 = nn.Conv2d(num_feat, num_feat, kernel_size=3, stride=1, padding=1, bias=True)
        self.relu = nn.ReLU(inplace=True)

        # Initialize weights if pytorch_init is False
        if not pytorch_init:
            default_init_weights([self.conv1, self.conv2], scale=0.1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the residual block.

        Args:
            x (torch.Tensor): Input tensor.

        Returns:
            torch.Tensor: Output tensor after applying the residual connection.
        """
        identity = x
        out = self.conv2(self.relu(self.conv1(x)))
        return identity + out * self.res_scale


class Upsample(nn.Sequential):
    """
    Upsample module for increasing the spatial resolution of feature maps.

    Args:
        scale (int): Scale factor for upsampling. Supported scales: powers of 2 (2^n) and 3.
        num_feat (int): Number of input feature channels.
    
    Raises:
        ValueError: If the provided scale is not a power of 2 or 3.
    """

    def __init__(self, scale: int, num_feat: int) -> None:
        """
        Initialize the upsample layers based on the given scale and feature dimensions.

        Args:
            scale (int): The scaling factor. Must be 2^n or 3.
            num_feat (int): The number of feature channels.
        """
        layers = []

        if (scale & (scale - 1)) == 0:  # Check if scale is a power of 2
            num_upsamples = int(math.log2(scale))
            for _ in range(num_upsamples):
                layers.append(nn.Conv2d(num_feat, 4 * num_feat, kernel_size=3, stride=1, padding=1))
                layers.append(nn.PixelShuffle(2))
        elif scale == 3:
            layers.append(nn.Conv2d(num_feat, 9 * num_feat, kernel_size=3, stride=1, padding=1))
            layers.append(nn.PixelShuffle(3))
        else:
            raise ValueError(f'Scale {scale} is not supported. Supported scales: 2^n and 3.')

        super().__init__(*layers)


def flow_warp(
    x: Tensor, 
    flow: Tensor, 
    interp_mode: str = 'bilinear', 
    padding_mode: str = 'zeros', 
    align_corners: bool = True
) -> Tensor:
    """
    Warp an image or feature map with optical flow.

    Args:
        x (Tensor): Input tensor of shape (n, c, h, w) representing an image or feature map.
        flow (Tensor): Flow tensor of shape (n, h, w, 2), where the last dimension represents the displacement.
        interp_mode (str, optional): Interpolation mode ('nearest' or 'bilinear'). Default is 'bilinear'.
        padding_mode (str, optional): Padding mode ('zeros', 'border', or 'reflection'). Default is 'zeros'.
        align_corners (bool, optional): Whether to align corners. Default is True for compatibility with versions of PyTorch before 1.3.

    Returns:
        Tensor: Warped image or feature map of shape (n, c, h, w).
    """
    assert x.size()[-2:] == flow.size()[1:3], "Input and flow spatial sizes must match"
    n, c, h, w = x.size()

    # Create mesh grid for pixel coordinates
    grid = _create_meshgrid(h, w, x)

    # Add flow to the grid to create the warped grid
    vgrid = grid + flow

    # Normalize the grid to the range [-1, 1]
    vgrid_scaled = _normalize_grid(vgrid, h, w)

    # Perform grid sampling with the given interpolation and padding modes
    output = F.grid_sample(x, vgrid_scaled, mode=interp_mode, padding_mode=padding_mode, align_corners=align_corners)

    return output


def _create_meshgrid(h: int, w: int, x: Tensor) -> Tensor:
    """Create a meshgrid for image coordinates.

    Args:
        h (int): Height of the image.
        w (int): Width of the image.
        x (Tensor): Input tensor to derive the device and data type.

    Returns:
        Tensor: A meshgrid tensor of shape (h, w, 2).
    """
    grid_y, grid_x = torch.meshgrid(torch.arange(0, h).type_as(x), torch.arange(0, w).type_as(x))
    grid = torch.stack((grid_x, grid_y), 2).float()  # Shape: (h, w, 2)
    grid.requires_grad = False
    return grid


def _normalize_grid(vgrid: Tensor, h: int, w: int) -> Tensor:
    """Normalize the grid to the range [-1, 1] for grid_sample.

    Args:
        vgrid (Tensor): The grid with optical flow applied.
        h (int): Height of the image.
        w (int): Width of the image.

    Returns:
        Tensor: Normalized grid of shape (n, h, w, 2).
    """
    vgrid_x = 2.0 * vgrid[:, :, :, 0] / max(w - 1, 1) - 1.0
    vgrid_y = 2.0 * vgrid[:, :, :, 1] / max(h - 1, 1) - 1.0
    return torch.stack((vgrid_x, vgrid_y), dim=3)


def resize_flow(
    flow: Tensor, 
    size_type: str, 
    sizes: List[Union[int, float]], 
    interp_mode: str = 'bilinear', 
    align_corners: bool = False
) -> Tensor:
    """
    Resize a flow according to the provided ratio or shape.

    Args:
        flow (Tensor): Precomputed flow of shape [N, 2, H, W].
        size_type (str): Either 'ratio' or 'shape'.
            - 'ratio': Resize by the provided ratio for height and width.
            - 'shape': Resize to the provided shape [out_h, out_w].
        sizes (list[int | float]): The resizing ratio or output size.
            - For 'ratio', sizes should be [ratio_h, ratio_w].
            - For 'shape', sizes should be [out_h, out_w].
        interp_mode (str, optional): Interpolation mode for resizing. Default is 'bilinear'.
        align_corners (bool, optional): Whether to align corners. Default is False.

    Returns:
        Tensor: Resized flow.
    
    Raises:
        ValueError: If size_type is not 'ratio' or 'shape'.
    """
    flow_h, flow_w = flow.shape[-2], flow.shape[-1]

    if size_type == 'ratio':
        output_h, output_w = _get_output_size_from_ratio(flow_h, flow_w, sizes)
    elif size_type == 'shape':
        output_h, output_w = sizes[0], sizes[1]
    else:
        raise ValueError(f"Invalid size_type '{size_type}'. Must be 'ratio' or 'shape'.")

    input_flow = _adjust_flow(flow.clone(), output_h, output_w, flow_h, flow_w)
    resized_flow = F.interpolate(input=input_flow, size=(output_h, output_w), mode=interp_mode, align_corners=align_corners)

    return resized_flow


def _get_output_size_from_ratio(flow_h: int, flow_w: int, sizes: List[float]) -> (int, int):
    """Calculate the output size based on resizing ratios."""
    output_h = int(flow_h * sizes[0])
    output_w = int(flow_w * sizes[1])
    return output_h, output_w


def _adjust_flow(flow: Tensor, output_h: int, output_w: int, flow_h: int, flow_w: int) -> Tensor:
    """Adjust flow values according to the new size by applying the appropriate ratio."""
    ratio_h = output_h / flow_h
    ratio_w = output_w / flow_w

    flow[:, 0, :, :] *= ratio_w  # Adjust x-direction flow
    flow[:, 1, :, :] *= ratio_h  # Adjust y-direction flow

    return flow


def pixel_unshuffle(x: Tensor, scale: int) -> Tensor:
    """
    Perform pixel unshuffle operation to downsample the input tensor by a given scale.

    Args:
        x (Tensor): Input tensor of shape (b, c, hh, hw), where hh and hw are the spatial dimensions.
        scale (int): Downsample ratio (the factor by which to reduce spatial dimensions).

    Returns:
        Tensor: The pixel unshuffled tensor with reduced spatial dimensions and increased channels.
    
    Raises:
        AssertionError: If the height or width of the input is not divisible by the scale factor.
    """
    b, c, hh, hw = x.size()
    out_channel = c * (scale ** 2)

    assert hh % scale == 0 and hw % scale == 0, "Input dimensions must be divisible by the scale factor."
    
    h, w = hh // scale, hw // scale

    # Reshape and permute to perform the pixel unshuffle operation
    x_view = x.view(b, c, h, scale, w, scale)
    return x_view.permute(0, 1, 3, 5, 2, 4).reshape(b, out_channel, h, w)


class DCNv2Pack(ModulatedDeformConvPack):
    """
    Modulated deformable convolution for deformable alignment.

    Unlike the official DCNv2Pack, this implementation generates offsets and masks from separate input features.

    Reference:
        Delving Deep into Deformable Alignment in Video Super-Resolution.
    """

    def forward(self, x: Tensor, feat: Tensor) -> Tensor:
        """
        Forward pass for the DCNv2Pack layer.

        Args:
            x (Tensor): Input feature map to be convolved.
            feat (Tensor): Feature map to generate offsets and masks.

        Returns:
            Tensor: The output feature map after applying deformable convolution.
        """
        out = self.conv_offset(feat)
        offset, mask = self._split_and_process_offsets(out)

        # Log a warning if the absolute mean of the offsets is too large
        offset_absmean = torch.mean(torch.abs(offset))
        if offset_absmean > 50:
            logger = get_root_logger()
            logger.warning(f'Offset absolute mean is {offset_absmean}, larger than 50.')

        return self._apply_deform_conv(x, offset, mask)

    def _split_and_process_offsets(self, out: Tensor) -> tuple[Tensor, Tensor]:
        """
        Split the output into offsets and mask, and apply sigmoid to the mask.

        Args:
            out (Tensor): The output from the offset convolution.

        Returns:
            tuple[Tensor, Tensor]: Processed offsets and masks.
        """
        o1, o2, mask = torch.chunk(out, 3, dim=1)
        offset = torch.cat((o1, o2), dim=1)
        mask = torch.sigmoid(mask)
        return offset, mask

    def _apply_deform_conv(self, x: Tensor, offset: Tensor, mask: Tensor) -> Tensor:
        """
        Apply deformable convolution based on PyTorch version.

        Args:
            x (Tensor): Input feature map.
            offset (Tensor): Offsets for deformable convolution.
            mask (Tensor): Modulation masks for deformable convolution.

        Returns:
            Tensor: Output feature map after deformable convolution.
        """
        if LooseVersion(torchvision.__version__) >= LooseVersion('0.9.0'):
            return torchvision.ops.deform_conv2d(
                x, offset, self.weight, self.bias, self.stride, self.padding, self.dilation, mask
            )
        else:
            return modulated_deform_conv(
                x, offset, mask, self.weight, self.bias, self.stride, self.padding,
                self.dilation, self.groups, self.deformable_groups
            )


def _no_grad_trunc_normal_(
    tensor: Tensor, 
    mean: float, 
    std: float, 
    a: float, 
    b: float
) -> Tensor:
    """
    Fills the input tensor with values drawn from a truncated normal distribution, 
    with mean `mean` and standard deviation `std`, truncated between `a` and `b`.

    Args:
        tensor (Tensor): An n-dimensional `torch.Tensor` to be filled.
        mean (float): The mean of the normal distribution.
        std (float): The standard deviation of the normal distribution.
        a (float): The minimum value for truncation.
        b (float): The maximum value for truncation.

    Returns:
        Tensor: The tensor filled with values drawn from the truncated normal distribution.
    
    Raises:
        Warning: If the `mean` is more than 2 standard deviations away from the truncation boundaries.

    Reference:
        This method is based on the paper: https://people.sc.fsu.edu/~jburkardt/presentations/truncated_normal.pdf
    """
    
    def norm_cdf(x: float) -> float:
        """Compute the cumulative distribution function for a standard normal distribution."""
        return (1. + math.erf(x / math.sqrt(2.))) / 2.

    # Warn if the mean is far from the truncation bounds
    if mean < a - 2 * std or mean > b + 2 * std:
        warnings.warn(
            'Mean is more than 2 std deviations away from the bounds [a, b]. '
            'The distribution of values may be incorrect.',
            stacklevel=2
        )

    with torch.no_grad():
        # Get the lower and upper cumulative distribution function values
        low, up = norm_cdf((a - mean) / std), norm_cdf((b - mean) / std)

        # Uniformly fill tensor with values from the transformed [low, up]
        tensor.uniform_(2 * low - 1, 2 * up - 1)

        # Apply inverse CDF transform for the normal distribution
        tensor.erfinv_()

        # Scale by the standard deviation and shift by the mean
        tensor.mul_(std * math.sqrt(2.))
        tensor.add_(mean)

        # Clamp the values to ensure they're within the [a, b] bounds
        tensor.clamp_(min=a, max=b)

    return tensor


def trunc_normal_(
    tensor: Tensor, 
    mean: float = 0.0, 
    std: float = 1.0, 
    a: float = -2.0, 
    b: float = 2.0
) -> Tensor:
    """
    Fills the input tensor with values drawn from a truncated normal distribution.

    The values are drawn from a normal distribution with mean `mean` and 
    standard deviation `std`, but values outside the interval [a, b] are redrawn 
    until they fall within the bounds.

    Args:
        tensor (Tensor): An n-dimensional tensor to be filled.
        mean (float, optional): The mean of the normal distribution. Default is 0.0.
        std (float, optional): The standard deviation of the normal distribution. Default is 1.0.
        a (float, optional): The minimum cutoff value. Default is -2.0.
        b (float, optional): The maximum cutoff value. Default is 2.0.

    Returns:
        Tensor: The input tensor filled with values from the truncated normal distribution.

    Example:
        >>> w = torch.empty(3, 5)
        >>> trunc_normal_(w)
    """
    return _no_grad_trunc_normal_(tensor, mean, std, a, b)


def _ntuple(n: int) -> Callable[[Any], Tuple[Any, ...]]:
    """
    Returns a function that converts the input into a tuple of length `n`.

    Args:
        n (int): The number of times to repeat the input value if it is not already an iterable.

    Returns:
        Callable[[Any], Tuple[Any, ...]]: A function that takes an input and returns a tuple of length `n`.
    """
    def parse(x: Any) -> Tuple[Any, ...]:
        if isinstance(x, collections.abc.Iterable) and not isinstance(x, str):
            return tuple(x)
        return tuple(repeat(x, n))

    return parse


# Specific tuple converters
to_1tuple = _ntuple(1)
to_2tuple = _ntuple(2)
to_3tuple = _ntuple(3)
to_4tuple = _ntuple(4)

# Generic n-tuple converter
to_ntuple = _ntuple