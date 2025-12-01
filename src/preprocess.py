"""
Image preprocessing module for whiteboard math photos.
Applies classical CV techniques to clean images before LaTeX recognition.

Note: pix2tex works best with clean, high-contrast images that preserve
the original character shapes. Aggressive binary thresholding can destroy
important details that the model needs.
"""

# OpenCV for image processing operations (blur, threshold, transform, etc.)
import cv2
# NumPy for numerical operations and array handling
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
    # Read the image from disk - OpenCV loads it in BGR format by default
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Could not read image from {input_path}")
    
    # Convert from BGR color to grayscale - simplifies processing and reduces data
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply light blur to reduce noise - small 3x3 kernel keeps details while smoothing
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # Enhance contrast with CLAHE - divides image into tiles and adjusts contrast locally
    # Clip limit prevents noise amplification, tile size balances local vs global effects
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(blurred)
    
    # Optionally convert to pure black/white if aggressive mode is on
    # Usually skipped since pix2tex works better with grayscale images
    if aggressive:
        # Otsu's method automatically finds the best threshold value
        _, enhanced = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Detect and correct image rotation if it's tilted
    # First create a binary version just to find lines (we don't keep this)
    _, temp_binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # Hough transform finds straight lines in the image
    lines = cv2.HoughLines(temp_binary, 1, np.pi / 180, 200)
    
    if lines is not None and len(lines) > 0:
        # Collect angles from detected lines to find the overall tilt
        angles = []
        for line in lines[:20]:  # Sample first 20 lines for speed
            rho, theta = line[0]
            # Convert from radians and adjust to get rotation angle
            angle = (theta * 180 / np.pi) - 90
            if abs(angle) < 45:  # Ignore extreme angles (probably errors)
                angles.append(angle)
        
        if angles:
            # Average all the angles to get the overall skew
            avg_angle = np.mean(angles)
            # Only rotate if there's a meaningful tilt (> 1 degree)
            if abs(avg_angle) > 1.0:
                # Create rotation matrix centered on image
                center = (enhanced.shape[1] // 2, enhanced.shape[0] // 2)
                M = cv2.getRotationMatrix2D(center, avg_angle, 1.0)
                # Apply rotation and fill edges with replicated pixels (no black borders)
                enhanced = cv2.warpAffine(enhanced, M, (enhanced.shape[1], enhanced.shape[0]), 
                                          borderMode=cv2.BORDER_REPLICATE)
    
    # Resize to a standard size that the model likes (around 800px width works well)
    # Only shrink if image is larger - keep small images as-is to preserve quality
    height, width = enhanced.shape
    target_width = 800  # Sweet spot for pix2tex - not too big, not too small
    
    if width > target_width:
        # Calculate height to keep proportions correct
        aspect_ratio = height / width
        target_height = int(target_width * aspect_ratio)
        # INTER_AREA is best for shrinking - gives clean results
        resized = cv2.resize(enhanced, (target_width, target_height), interpolation=cv2.INTER_AREA)
    else:
        resized = enhanced  # Already small enough, no need to resize
    
    # Write the final processed image to disk
    cv2.imwrite(output_path, resized)
    
    return output_path

