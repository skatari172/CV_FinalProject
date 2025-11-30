"""
Image preprocessing module for whiteboard math photos.
Applies classical CV techniques to clean images before LaTeX recognition.

Note: pix2tex works best with clean, high-contrast images that preserve
the original character shapes. Aggressive binary thresholding can destroy
important details that the model needs.
"""

import cv2
import numpy as np


def preprocess_image(input_path: str, output_path: str, aggressive: bool = False) -> str:
    """
    Preprocess a whiteboard image for LaTeX recognition.
    
    Steps:
    1. Read image
    2. Convert to grayscale
    3. Light noise reduction
    4. Enhance contrast (CLAHE)
    5. Optional deskew using Hough transform
    6. Resize to reasonable dimensions
    7. Save processed image
    
    Args:
        input_path: Path to input whiteboard image
        output_path: Path to save preprocessed image
        aggressive: If True, apply binary thresholding (may reduce accuracy)
        
    Returns:
        output_path: Path to saved preprocessed image
    """
    # Read the image
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Could not read image from {input_path}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Light Gaussian blur to reduce noise (smaller kernel)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # Enhance contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
    # This improves visibility without destroying character shapes
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(blurred)
    
    # Optional: Apply binary threshold only if aggressive mode is enabled
    if aggressive:
        # Use Otsu's method for automatic threshold selection
        _, enhanced = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Deskew using Hough transform (optional, simple implementation)
    # Create a temporary binary image just for line detection
    _, temp_binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    lines = cv2.HoughLines(temp_binary, 1, np.pi / 180, 200)
    
    if lines is not None and len(lines) > 0:
        # Calculate average angle
        angles = []
        for line in lines[:20]:  # Use first 20 lines
            rho, theta = line[0]
            angle = (theta * 180 / np.pi) - 90
            if abs(angle) < 45:  # Only consider reasonable angles
                angles.append(angle)
        
        if angles:
            avg_angle = np.mean(angles)
            # Only deskew if angle is significant (> 1 degree)
            if abs(avg_angle) > 1.0:
                center = (enhanced.shape[1] // 2, enhanced.shape[0] // 2)
                M = cv2.getRotationMatrix2D(center, avg_angle, 1.0)
                enhanced = cv2.warpAffine(enhanced, M, (enhanced.shape[1], enhanced.shape[0]), 
                                          borderMode=cv2.BORDER_REPLICATE)
    
    # Resize to reasonable dimensions while maintaining aspect ratio
    # pix2tex works well with images around 400-1000px width
    height, width = enhanced.shape
    target_width = 800  # Reduced from 1500 for better model performance
    
    if width > target_width:
        aspect_ratio = height / width
        target_height = int(target_width * aspect_ratio)
        resized = cv2.resize(enhanced, (target_width, target_height), interpolation=cv2.INTER_AREA)
    else:
        resized = enhanced
    
    # Save the processed image
    cv2.imwrite(output_path, resized)
    
    return output_path

