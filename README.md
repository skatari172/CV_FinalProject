# Whiteboard to LaTeX Converter

Test -> https://www.text2latex.com/

A simple computer vision project that converts whiteboard math photos into LaTeX format using classical image preprocessing and the pix2tex pretrained model.

## Overview

This project takes a whiteboard image as input, preprocesses it using OpenCV, and uses the pix2tex model to recognize mathematical equations and convert them to LaTeX format.

## Features

- **Classical CV Preprocessing**: Grayscale conversion, blur, adaptive threshold, noise removal, deskew, and resizing
- **Pretrained Model**: Uses the official pix2tex model for LaTeX recognition
- **Web Application**: Beautiful web interface with drag-and-drop image upload and LaTeX rendering
- **Simple CLI**: Easy-to-use command-line interface
- **Minimal Setup**: Clean project structure

## Requirements

- Python 3.6+
- OpenCV
- pix2tex
- PyTorch
- NumPy
- Pillow
- Flask (for web app)

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

### Web Application (Recommended)

Start the Flask web server:

```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5001
```

**Note**: Port 5001 is used instead of 5000 to avoid conflicts with macOS AirPlay Receiver.

The web interface allows you to:
- Upload images via drag-and-drop or file picker
- Preview the uploaded image
- Process the image and get LaTeX output
- View both the raw LaTeX code and rendered mathematical formula
- Copy the LaTeX code to clipboard

### Command Line Interface

For CLI usage:

```bash
python main.py <image_path>
```

#### Example

```bash
python main.py samples/example.jpg
```

The script will:
1. Preprocess the image (grayscale, blur, threshold, noise removal, deskew, resize)
2. Run the pix2tex model on the preprocessed image
3. Print the LaTeX output to the console
4. Save the LaTeX result to `output.tex`

#### Output

- Console output: Displays the recognized LaTeX string
- File output: Saves LaTeX to `output/output.tex`

## Project Structure

```
whiteboard-tex-simple/
├── app.py                 # Web application entry point
├── main.py                # CLI entry point
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── src/                   # Core modules
│   ├── __init__.py
│   ├── preprocess.py      # Image preprocessing functions
│   └── model_infer.py     # Pix2Tex model wrapper
├── web/                   # Web application
│   ├── app.py             # Flask application
│   ├── templates/
│   │   └── index.html     # Web app frontend
│   └── static/
│       ├── css/
│       │   └── style.css  # Web app styling
│       └── js/
│           └── app.js     # Web app JavaScript
├── samples/               # Sample images
│   └── example.jpg
├── output/                # CLI output directory (auto-created)
└── uploads/               # Web app upload directory (auto-created)
```

## File Descriptions

### Core Modules (`src/`)

#### `src/preprocess.py`
Contains the `preprocess_image()` function that applies classical computer vision techniques:
- Grayscale conversion
- Gaussian blur
- Adaptive thresholding
- Optional deskew using Hough transform
- Morphological operations for noise removal
- Resizing to fixed width (1500px)

#### `src/model_infer.py`
Contains the `Pix2TexModel` class that:
- Loads the pretrained pix2tex model
- Provides a `predict()` method for LaTeX recognition

### Entry Points

#### `main.py`
CLI script that:
- Accepts input image path
- Orchestrates preprocessing and inference
- Outputs LaTeX result to console and file
- Saves output to `output/output.tex`

#### `app.py`
Web application entry point that:
- Imports and runs the Flask application
- Starts the web server on port 5000

### Web Application (`web/`)

#### `web/app.py`
Flask application that:
- Provides a web interface for image upload
- Handles file uploads and processing
- Returns LaTeX results as JSON
- Renders results in the browser with MathJax

#### `web/templates/index.html`
Main web interface with:
- Drag-and-drop image upload
- Image preview
- LaTeX code display
- Rendered mathematical formula using MathJax

#### `web/static/css/style.css`
Modern, responsive styling for the web interface

#### `web/static/js/app.js`
Client-side JavaScript for:
- File upload handling
- Image preview
- API communication
- LaTeX rendering

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
- Reducing the resize width in `src/preprocess.py` (default: 1500px)

### Dependency Conflicts
If you encounter dependency conflicts, use a fresh virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## License

This project is provided as-is for educational purposes.

