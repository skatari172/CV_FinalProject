"""
Core modules for whiteboard to LaTeX conversion.

This package makes it easy to import the main functions/classes from other modules.
Instead of: from src.preprocess import preprocess_image
You can do: from src import preprocess_image
"""

# Import the main functions so they're available at package level
from .preprocess import preprocess_image
from .model_infer import Pix2TexModel

# Explicitly define what gets exported when someone does "from src import *"
__all__ = ['preprocess_image', 'Pix2TexModel']

