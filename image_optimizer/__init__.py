# Image Optimizer Tool
# Properly resizes images for various app uses with minimal quality loss

from .optimizer import ImageOptimizer
from .presets import SIZE_PRESETS, get_preset, list_presets
from .strategies import ResizeStrategy

__all__ = ['ImageOptimizer', 'SIZE_PRESETS', 'get_preset', 'list_presets', 'ResizeStrategy']
__version__ = '1.0.0'
