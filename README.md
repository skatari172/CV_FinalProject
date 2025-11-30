# Whiteboard to LaTeX Converter

A simple computer vision project that converts whiteboard math photos into LaTeX format using classical image preprocessing and the pix2tex pretrained model.

## Overview

This project takes a whiteboard image as input, preprocesses it using OpenCV, and uses the pix2tex model to recognize mathematical equations and convert them to LaTeX format.

## Features

- **Classical CV Preprocessing**: Grayscale conversion, blur, adaptive threshold, noise removal, deskew, and resizing
- **Pretrained Model**: Uses the official pix2tex model for LaTeX recognition
- **Simple CLI**: Easy-to-use command-line interface
- **Minimal Setup**: Only 3 main Python files

## Requirements

- Python 3.6+
- OpenCV
- pix2tex
- PyTorch
- NumPy
- Pillow

## Setup

### 1. Create a Virtual Environment (Recommended)

It's highly recommended to use a virtual environment to isolate dependencies:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: The first run will download the pretrained pix2tex model (~500MB), which may take a few minutes.

## Usage

### Basic Usage

```bash
python main.py <image_path>
```

### Example

```bash
python main.py samples/example.jpg
```

The script will:
1. Preprocess the image (grayscale, blur, threshold, noise removal, deskew, resize)
2. Run the pix2tex model on the preprocessed image
3. Print the LaTeX output to the console
4. Save the LaTeX result to `output.tex`

### Output

- Console output: Displays the recognized LaTeX string
- File output: Saves LaTeX to `output.tex` in the project root

## Project Structure

```
whiteboard-tex-simple/
├── preprocess.py          # Image preprocessing functions
├── model_infer.py         # Pix2Tex model wrapper
├── main.py                # CLI entry point
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── samples/
    └── example.jpg        # Sample whiteboard image
```

## File Descriptions

### `preprocess.py`
Contains the `preprocess_image()` function that applies classical computer vision techniques:
- Grayscale conversion
- Gaussian blur
- Adaptive thresholding
- Optional deskew using Hough transform
- Morphological operations for noise removal
- Resizing to fixed width (1500px)

### `model_infer.py`
Contains the `Pix2TexModel` class that:
- Loads the pretrained pix2tex model
- Provides a `predict()` method for LaTeX recognition

### `main.py`
Main CLI script that:
- Accepts input image path
- Orchestrates preprocessing and inference
- Outputs LaTeX result to console and file

## Notes

- **Single-line processing**: The project treats the entire whiteboard as one equation line (no multi-line detection)
- **First run**: The pix2tex model will be downloaded automatically on first use (~500MB)
- **Image format**: Supports common image formats (JPG, PNG, etc.)

## Troubleshooting

### Model Download Issues
If the model fails to download automatically, you may need to download it manually. Check the [pix2tex documentation](https://github.com/lukas-blecher/LaTeX-OCR) for details.

### Memory Issues
If you encounter memory issues, try:
- Processing smaller images
- Reducing the resize width in `preprocess.py` (default: 1500px)

### Dependency Conflicts
If you encounter dependency conflicts, use a fresh virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## License

This project is provided as-is for educational purposes.

