# Image Detection

## Functional Requirements

### 1. Batch Image Processing

The tool processes multiple image files at once from a specified folder.

- **Default Behavior**: Automatically scans and processes all images in the `data` folder
- **Custom Folder Support**: Users can specify a different folder path when running the tool
- **Supported Formats**: Works with common image formats including JPG, JPEG, PNG, GIF, BMP, WEBP, and TIFF

### 2. Image Type Detection

The tool categorizes each image into one of four types:

#### 2.1 All Black Image

- **Description**: The entire image is completely black
- **Output**: Displays "All black"

#### 2.2 All White Image

- **Description**: The entire image is completely white
- **Output**: Displays "All white"

#### 2.3 Single Color Image

- **Description**: The entire image is a single solid color (not black or white), such as a solid gray, red, or blue
- **Output**: Displays "Single color (gray value: X)" where X indicates the brightness level of that color (ranging from 1 to 254)

#### 2.4 Mixed Pixels Image

- **Description**: The image contains multiple different colors or shades
- **Output**: Displays "Mixed pixels"

### 3. Image Dimension Information

For each processed image, the tool displays:

- **Image filename**
- **Image dimensions** (width and height in pixels)
- **Detected image type**

**Example Output**: `150x150.jpg (150x150): Mixed pixels`

This means the file "150x150.jpg" is 150 pixels wide by 150 pixels tall, and contains mixed pixels.

### 4. Processing Time Statistics

After processing all images, the tool displays the total time taken to complete the analysis.

- **Display Location**: Shown as the last line of output
- **Format**: "Total processing time: X" where X shows the actual duration (e.g., "10.57 milliseconds")
