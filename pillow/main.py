#!/usr/bin/env python3
"""
Image Detection Tool

This tool processes multiple image files and categorizes them into:
- All black images
- All white images
- Single color images
- Mixed pixels images
"""

import os
import sys
import time
from pathlib import Path
from PIL import Image
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


def calculate_gray_value(r, g, b):
    """
    Calculate the gray value (brightness) of an RGB color.
    Uses the standard luminance formula: 0.299*R + 0.587*G + 0.114*B
    
    Args:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)
        
    Returns:
        int: Gray value from 0 to 255
    """
    return int(0.299 * r + 0.587 * g + 0.114 * b)


def detect_image_type(image):
    """
    Detect the type of an image.
    
    Args:
        image: PIL Image object
        
    Returns:
        str: Image type description
    """
    # Convert to RGB if necessary (handles RGBA, L, P modes)
    if image.mode != 'RGB':
        rgb_image = image.convert('RGB')
    else:
        rgb_image = image
    
    # Get all pixel data
    pixels = list(rgb_image.getdata())
    
    if not pixels:
        return "Mixed pixels"
    
    # Get the first pixel as reference
    first_pixel = pixels[0]
    first_r, first_g, first_b = first_pixel
    first_gray = calculate_gray_value(first_r, first_g, first_b)
    
    # Check if all pixels are the same
    all_same = all(pixel == first_pixel for pixel in pixels)
    
    if all_same:
        # All pixels are identical
        if first_r == 0 and first_g == 0 and first_b == 0:
            return "All black"
        elif first_r == 255 and first_g == 255 and first_b == 255:
            return "All white"
        else:
            # Single color (not black or white)
            gray_value = first_gray
            # Ensure gray value is in range 1-254 (not black or white)
            if gray_value == 0:
                gray_value = 1
            elif gray_value == 255:
                gray_value = 254
            return f"Single color (gray value: {gray_value})"
    else:
        # Check if all pixels have the same gray value (but different RGB combinations)
        all_same_gray = all(calculate_gray_value(*pixel) == first_gray for pixel in pixels)
        
        if all_same_gray:
            # All pixels have the same brightness but different colors
            # This is still considered "single color" in terms of brightness
            gray_value = first_gray
            if gray_value == 0:
                gray_value = 1
            elif gray_value == 255:
                gray_value = 254
            return f"Single color (gray value: {gray_value})"
        else:
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
        with Image.open(image_path) as img:
            width, height = img.size
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

