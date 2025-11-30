"""
Main CLI script for whiteboard to LaTeX conversion.
"""

import sys
import os
from preprocess import preprocess_image
from model_infer import Pix2TexModel


def main():
    """Main entry point for the whiteboard to LaTeX converter."""
    # Check if input image path is provided
    if len(sys.argv) != 2:
        print("Usage: python main.py <image_path>")
        print("Example: python main.py samples/example.jpg")
        sys.exit(1)
    
    input_image_path = sys.argv[1]
    
    # Validate input file exists
    if not os.path.exists(input_image_path):
        print(f"Error: Image file not found: {input_image_path}")
        sys.exit(1)
    
    # Preprocess the image
    print(f"Preprocessing image: {input_image_path}")
    preprocessed_path = "preprocessed_temp.png"
    
    try:
        preprocess_image(input_image_path, preprocessed_path)
        print("Image preprocessed successfully!")
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        sys.exit(1)
    
    # Initialize model
    try:
        model = Pix2TexModel()
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)
    
    # Run inference
    print("Running LaTeX recognition...")
    try:
        latex_result = model.predict(preprocessed_path)
    except Exception as e:
        print(f"Error during inference: {e}")
        sys.exit(1)
    
    # Print result
    print("\n" + "="*50)
    print("LaTeX Output:")
    print("="*50)
    print(latex_result)
    print("="*50 + "\n")
    
    # Save to output.tex
    output_file = "output.tex"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_result)
        print(f"LaTeX saved to {output_file}")
    except Exception as e:
        print(f"Error saving output: {e}")
        sys.exit(1)
    
    # Clean up temporary preprocessed image
    try:
        if os.path.exists(preprocessed_path):
            os.remove(preprocessed_path)
    except Exception as e:
        print(f"Warning: Could not remove temporary file: {e}")


if __name__ == "__main__":
    main()

