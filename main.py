"""
Main CLI script for whiteboard to LaTeX conversion.
Run from command line: python main.py path/to/image.jpg
"""

# System utilities for command line arguments and file operations
import sys
import os
# Import our preprocessing function that cleans up the image
from src.preprocess import preprocess_image
# Import the model wrapper that runs the LaTeX recognition
from src.model_infer import Pix2TexModel


def main():
    """
    Main workflow: validate input, preprocess image, run model, save result.
    This is the command-line interface version of the application.
    """
    # Make sure user provided an image path as an argument
    if len(sys.argv) != 2:
        print("Usage: python main.py <image_path>")
        print("Example: python main.py samples/example.jpg")
        sys.exit(1)
    
    input_image_path = sys.argv[1]
    
    # Verify the file actually exists before we try to process it
    if not os.path.exists(input_image_path):
        print(f"Error: Image file not found: {input_image_path}")
        sys.exit(1)
    
    # Step 1: Clean up and enhance the image using CV techniques
    print(f"Preprocessing image: {input_image_path}")
    os.makedirs("output", exist_ok=True)
    preprocessed_path = os.path.join("output", "preprocessed_temp.png")
    
    try:
        preprocess_image(input_image_path, preprocessed_path)
        print("Image preprocessed successfully!")
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        sys.exit(1)
    
    # Step 2: Load the deep learning model (this takes a few seconds the first time)
    try:
        model = Pix2TexModel()
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)
    
    # Step 3: Run the model on the preprocessed image to get LaTeX
    print("Running LaTeX recognition...")
    try:
        latex_result = model.predict(preprocessed_path)
    except Exception as e:
        print(f"Error during inference: {e}")
        sys.exit(1)
    
    # Display the result in the terminal
    print("\n" + "="*50)
    print("LaTeX Output:")
    print("="*50)
    print(latex_result)
    print("="*50 + "\n")
    
    # Step 4: Save the LaTeX to a file so user can use it later
    os.makedirs("output", exist_ok=True)
    output_file = os.path.join("output", "output.tex")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_result)
        print(f"LaTeX saved to {output_file}")
    except Exception as e:
        print(f"Error saving output: {e}")
        sys.exit(1)
    
    # Clean up the temporary preprocessed image file
    try:
        if os.path.exists(preprocessed_path):
            os.remove(preprocessed_path)
    except Exception as e:
        print(f"Warning: Could not remove temporary file: {e}")


if __name__ == "__main__":
    main()

