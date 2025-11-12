#!/usr/bin/env python3
"""
Image Detection Tool

This tool processes multiple image files and categorizes them into:
- All black images
- All white images
- Single color images
- Mixed pixels images
"""

import sys
import time
from pathlib import Path
import cv2
import numpy as np
import argparse


# Supported image formats
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}


def is_image_file(filepath):
    """
    Check if a file is a supported image format.
    
    Args:
        filepath: Path to the file
        
    Returns:
        bool: True if the file is a supported image format
    """
    return filepath.suffix.lower() in SUPPORTED_FORMATS


def get_image_files(folder_path):
    """
    Get all image files from the specified folder.
    
    Args:
        folder_path: Path to the folder containing images
        
    Returns:
        list: List of image file paths
    """
    folder = Path(folder_path)
    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        sys.exit(1)
    
    if not folder.is_dir():
        print(f"Error: '{folder_path}' is not a directory.")
        sys.exit(1)
    
    image_files = [f for f in folder.iterdir() if f.is_file() and is_image_file(f)]
    return sorted(image_files)


def calculate_gray_value(b, g, r):
    """
    Calculate the gray value (brightness) of a BGR color.
    Uses the standard luminance formula: 0.299*R + 0.587*G + 0.114*B
    
    Args:
        b: Blue component (0-255)
        g: Green component (0-255)
        r: Red component (0-255)
        
    Returns:
        int: Gray value from 0 to 255
    """
    return int(0.299 * r + 0.587 * g + 0.114 * b)


def normalize_gray_value(gray_value):
    """
    Normalize gray value to range 1-254 for single color images.
    
    Args:
        gray_value: Gray value (0-255)
        
    Returns:
        int: Normalized gray value (1-254)
    """
    if gray_value == 0:
        return 1
    elif gray_value == 255:
        return 254
    return gray_value


def detect_image_type(img):
    """
    Detect the type of an image.
    
    Args:
        img: OpenCV image (numpy array in BGR format)
        
    Returns:
        str: Image type description
    """
    if img is None or img.size == 0:
        return "Mixed pixels"
    
    # Convert to BGR if necessary (handle grayscale, RGBA, etc.)
    if len(img.shape) == 2:
        # Grayscale image
        bgr_img = None
        gray_values = img
    elif img.shape[2] == 4:
        # RGBA image, convert to BGR
        bgr_img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        gray_values = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    elif img.shape[2] == 3:
        # Already BGR
        bgr_img = img
        gray_values = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    else:
        return "Mixed pixels"
    
    # Check if all pixels have the same gray value
    unique_gray = np.unique(gray_values)
    if len(unique_gray) == 1:
        gray_value = int(unique_gray[0])
        if gray_value == 0:
            return "All black"
        elif gray_value == 255:
            return "All white"
        else:
            # gray_value is already in range 1-254 (0 and 255 handled above)
            return f"Single color (gray value: {gray_value})"
    
    # For BGR images, check if all pixels are identical (same RGB combination)
    if bgr_img is not None:
        pixels = bgr_img.reshape(-1, 3)
        first_pixel = pixels[0]
        if np.all(pixels == first_pixel):
            b, g, r = first_pixel[0], first_pixel[1], first_pixel[2]
            if b == 0 and g == 0 and r == 0:
                return "All black"
            elif b == 255 and g == 255 and r == 255:
                return "All white"
            else:
                gray_value = calculate_gray_value(b, g, r)
                return f"Single color (gray value: {normalize_gray_value(gray_value)})"
    
    return "Mixed pixels"


def process_image(image_path):
    """
    Process a single image and return its information.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        tuple: (filename, width, height, image_type) or None if error
    """
    try:
        img = cv2.imread(str(image_path))
        if img is None:
            print(f"Error processing {image_path.name}: Could not read image file.", file=sys.stderr)
            return None
        
        height, width = img.shape[:2]
        image_type = detect_image_type(img)
        filename = image_path.name
        return (filename, width, height, image_type)
    except Exception as e:
        print(f"Error processing {image_path.name}: {e}", file=sys.stderr)
        return None


def process_images(folder_path):
    """
    Process all images in the specified folder.
    
    Args:
        folder_path: Path to the folder containing images
    """
    image_files = get_image_files(folder_path)
    
    if not image_files:
        print(f"No supported image files found in '{folder_path}'.")
        print(f"Supported formats: {', '.join(sorted(SUPPORTED_FORMATS))}")
        return
    
    # Record start time
    start_time = time.perf_counter()
    
    # Process each image
    results = []
    for image_file in image_files:
        result = process_image(image_file)
        if result:
            results.append(result)
    
    # Record end time
    end_time = time.perf_counter()
    processing_time_ms = (end_time - start_time) * 1000
    
    # Display results
    for filename, width, height, image_type in results:
        print(f"{filename} ({width}x{height}): {image_type}")
    
    # Display processing time
    print(f"Total processing time: {processing_time_ms:.2f} milliseconds")


def main():
    """
    Main entry point for the image detection tool.
    """
    # Get the default data folder path (project root/data)
    script_dir = Path(__file__).parent
    default_data_path = script_dir.parent / 'data'
    
    parser = argparse.ArgumentParser(
        description='Image Detection Tool - Categorizes images into black, white, single color, or mixed pixels'
    )
    parser.add_argument(
        'folder',
        nargs='?',
        default=str(default_data_path),
        help='Path to the folder containing images (default: ../data)'
    )
    
    args = parser.parse_args()
    process_images(args.folder)


if __name__ == '__main__':
    main()

