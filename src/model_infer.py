"""
Model inference module for LaTeX recognition using pix2tex.
"""

from pix2tex.cli import LatexOCR
from PIL import Image


class Pix2TexModel:
    """
    Wrapper class for the pix2tex model.
    Loads the model once for efficient inference.
    """
    
    def __init__(self):
        """Initialize and load the pretrained pix2tex model."""
        print("Loading pix2tex model...")
        self.model = LatexOCR()
        print("Model loaded successfully!")
    
    def predict(self, image_path: str) -> str:
        """
        Predict LaTeX from a preprocessed image.
        
        Args:
            image_path: Path to the preprocessed image
            
        Returns:
            LaTeX string representation of the equation
        """
        # Load image as PIL Image for pix2tex (it expects PIL Image, not file path)
        img = Image.open(image_path)
        latex_result = self.model(img)
        return latex_result

