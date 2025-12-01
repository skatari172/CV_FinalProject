# Image to LaTeX Converter

A computer vision project that converts images of mathematical equations into LaTeX format using classical image preprocessing and the pix2tex pretrained model.

**Demo**: https://www.text2latex.com/

## Overview

This project takes an image containing a mathematical equation as input, preprocesses it using OpenCV, and uses the pix2tex model to recognize the equation and convert it to LaTeX format. It works best with screenshots of digital/online text, rendered equations from PDFs, textbooks, and other printed sources.

## Features

- **Classical CV Preprocessing**: Grayscale conversion, Gaussian blur, CLAHE contrast enhancement, deskewing, and resizing
- **Pretrained Model**: Uses the official pix2tex model for LaTeX recognition
- **Web Application**: Modern web interface with drag-and-drop image upload and real-time LaTeX rendering
- **Simple CLI**: Command-line interface for batch processing
- **Clean Architecture**: Well-organized project structure

## Supported Input Types

| Input Type | Expected Quality |
|------------|------------------|
| Screenshots of rendered LaTeX | ✅ Excellent |
| PDF equation screenshots | ✅ Excellent |
| Textbook photos | ✅ Good |
| Online math content | ✅ Good |
| Handwritten equations | ⚠️ Variable |

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
1. Preprocess the image (grayscale, blur, contrast enhancement, deskew, resize)
2. Run the pix2tex model on the preprocessed image
3. Print the LaTeX output to the console
4. Save the LaTeX result to `output/output.tex`

#### Output

- Console output: Displays the recognized LaTeX string
- File output: Saves LaTeX to `output/output.tex`

## Project Structure

```
image-to-latex/
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

## Computer Vision Techniques

This project applies several classical CV techniques for image preprocessing:

### 1. Grayscale Conversion
Reduces 3-channel color image to single-channel grayscale, simplifying processing.

### 2. Gaussian Blur
Applies a 3×3 Gaussian kernel to reduce high-frequency noise while preserving edges.

### 3. CLAHE (Contrast Limited Adaptive Histogram Equalization)
Enhances local contrast without over-amplifying noise. Divides image into tiles and applies histogram equalization with a clip limit.

### 4. Otsu's Thresholding
Automatic threshold selection for binarization by maximizing inter-class variance. Used for line detection during deskewing.

### 5. Hough Line Transform
Detects straight lines in the image using parametric representation (ρ, θ). Used to estimate skew angle.

### 6. Affine Transformation
Applies rotation matrix to correct detected skew angle, aligning text horizontally.

### 7. Image Resizing
Scales image to target width (800px) using INTER_AREA interpolation for optimal downscaling quality.

## File Descriptions

### Core Modules (`src/`)

#### `src/preprocess.py`
Contains the `preprocess_image()` function that applies the CV pipeline:
- Grayscale conversion
- Gaussian blur (3×3 kernel)
- CLAHE contrast enhancement
- Optional deskew using Hough transform
- Resizing to 800px width

#### `src/model_infer.py`
Contains the `Pix2TexModel` class that:
- Loads the pretrained pix2tex model
- Provides a `predict()` method for LaTeX recognition

### Entry Points

#### `main.py`
CLI script that orchestrates preprocessing and inference.

#### `app.py`
Web application entry point that starts the Flask server.

### Web Application (`web/`)

#### `web/app.py`
Flask application with routes for serving the UI and processing images.

#### `web/templates/index.html`
Frontend with drag-and-drop upload and MathJax rendering.

#### `web/static/`
CSS styling and JavaScript for the web interface.

## Notes

- **Single-line processing**: Treats the entire image as one equation (no multi-line detection)
- **Best results**: Use clean screenshots of rendered equations
- **First run**: Model downloads automatically (~500MB)
- **Image format**: Supports JPG, PNG, GIF, BMP

## Troubleshooting

### Model Download Issues
If the model fails to download automatically, check the [pix2tex documentation](https://github.com/lukas-blecher/LaTeX-OCR).

### Memory Issues
Try processing smaller images or reducing resize width in `src/preprocess.py`.

### Port Conflict
If port 5001 is in use, modify the port in `app.py`.

### Dependency Conflicts
Use a fresh virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## License

This project is provided as-is for educational purposes.
