"""
Model inference module for LaTeX recognition using pix2tex.
"""

# pix2tex provides the LatexOCR class - the actual deep learning model
from pix2tex.cli import LatexOCR
# PIL Image is needed because pix2tex expects Image objects, not file paths
from PIL import Image


class Pix2TexModel:
    """
    Wrapper class for the pix2tex model.
    Loads the model once when created, then reuses it for all predictions.
    This is much faster than loading the model every time.
    """
    
    def __init__(self):
        """Load the pretrained model into memory - this happens once at startup."""
        print("Loading pix2tex model...")
        # This downloads the model on first run (~500MB), then caches it
        self.model = LatexOCR()
        print("Model loaded successfully!")
    
    def predict(self, image_path: str) -> str:
        """
        Take a preprocessed image and convert it to LaTeX text.
        
        Args:
            image_path: Path to the preprocessed image file
            
        Returns:
            LaTeX string like "E = mc^2" or "\\frac{a}{b}"
        """
        # pix2tex needs a PIL Image object, not just a file path
        # This is important - passing a string path will cause errors
        img = Image.open(image_path)
        # Run the model - it uses a CNN encoder and transformer decoder internally
        latex_result = self.model(img)
        return latex_result

