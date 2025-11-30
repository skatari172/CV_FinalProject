"""
Image preprocessing module for whiteboard math photos.
Applies classical CV techniques to clean images before LaTeX recognition.
"""

import cv2
import numpy as np


def preprocess_image(input_path: str, output_path: str) -> str:
    """
    Preprocess a whiteboard image for LaTeX recognition.
    
    Steps:
    1. Read image
    2. Convert to grayscale
    3. Apply Gaussian blur
    4. Apply adaptive threshold (binary)
    5. Optional deskew using Hough transform
    6. Apply morphological opening to clean noise
    7. Resize to fixed width (1500px)
    8. Save processed image
    
    Args:
        input_path: Path to input whiteboard image
        output_path: Path to save preprocessed image
        
    Returns:
        output_path: Path to saved preprocessed image
    """
    # Read the image
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Could not read image from {input_path}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive threshold to create binary image
    # This helps separate text from background
    binary = cv2.adaptiveThreshold(
        blurred, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 
        11, 
        2
    )
    
    # Deskew using Hough transform (optional, simple implementation)
    # Find lines using Hough transform
    lines = cv2.HoughLines(binary, 1, np.pi / 180, 200)
    
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
            # Only deskew if angle is significant (> 0.5 degrees)
            if abs(avg_angle) > 0.5:
                center = (binary.shape[1] // 2, binary.shape[0] // 2)
                M = cv2.getRotationMatrix2D(center, avg_angle, 1.0)
                binary = cv2.warpAffine(binary, M, (binary.shape[1], binary.shape[0]))
    
    # Apply small morphological opening to clean noise
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # Resize to fixed width (1500px) while maintaining aspect ratio
    target_width = 1500
    height, width = cleaned.shape
    aspect_ratio = height / width
    target_height = int(target_width * aspect_ratio)
    
    resized = cv2.resize(cleaned, (target_width, target_height), interpolation=cv2.INTER_CUBIC)
    
    # Save the processed image
    cv2.imwrite(output_path, resized)
    
    return output_path

