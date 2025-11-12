# Image Detection Tool

A comprehensive image detection tool that categorizes images into four types: all black, all white, single color, or mixed pixels. This repository contains five different implementations using various technologies to compare performance and approaches.

## Overview

This project implements an image detection tool that processes multiple image files and categorizes them based on their pixel content. The tool supports batch processing and provides detailed information about each image, including dimensions and detected type.

For detailed functional requirements, please refer to [spec.md](spec.md).

## Features

- **Batch Processing**: Process multiple images from a folder at once
- **Image Type Detection**: Categorizes images into:
  - All black images
  - All white images
  - Single color images (with gray value)
  - Mixed pixels images
- **Dimension Information**: Displays width and height for each image
- **Performance Measurement**: Reports processing time for each run
- **Multiple Implementations**: Five different solutions for comparison

## Project Structure

```
.
├── cv2/          # Python + OpenCV implementation
├── goimage/      # Go + standard image library implementation
├── govips/       # Go + govips implementation
├── imageio/      # Python + imageio implementation
├── pillow/       # Python + Pillow implementation
├── data/         # Test image files
├── benchmark.py  # Benchmark script to compare all solutions
└── spec.md       # Functional requirements specification
```

## Solutions

This repository contains five different implementations:

### 1. govips (Go + govips)

Uses libvips through the govips Go bindings. High-performance image processing.

**Location**: `govips/`

**Requirements**:

- Go 1.21 or higher
- libvips (system dependency)
  - macOS: `brew install vips`
  - Linux: `sudo apt-get install libvips-dev` (Ubuntu/Debian) or `sudo yum install vips-devel` (CentOS/RHEL)

**Installation**:

```bash
cd govips
go mod tidy
go build -o govips main.go
```

**Usage**:

```bash
cd govips
go run main.go [folder_path]
# Or use the built executable:
./govips [folder_path]
```

For more details, see [govips/README.md](govips/README.md).

### 2. goimage (Go + standard image)

Uses Go standard library image packages. Lightweight with no external dependencies.

**Location**: `goimage/`

**Requirements**:

- Go 1.21 or higher

**Installation**:
No external dependencies required.

**Usage**:

```bash
cd goimage
go run main.go [folder_path]
# Or build first:
go build -o goimage main.go
./goimage [folder_path]
```

**Note**: Go standard library supports JPEG, PNG, and GIF formats only.

For more details, see [goimage/README.md](goimage/README.md).

### 3. pillow (Python + Pillow)

Uses Pillow (PIL) library for image processing.

**Location**: `pillow/`

**Requirements**:

- Python 3.7 or higher
- Pillow (>= 10.0.0)

**Installation**:

```bash
cd pillow
pip3 install -r requirements.txt
```

**Usage**:

```bash
python3 pillow/main.py [folder_path]
```

For more details, see [pillow/README.md](pillow/README.md).

### 4. cv2 (Python + OpenCV)

Uses OpenCV for image processing with NumPy for array operations.

**Location**: `cv2/`

**Requirements**:

- Python 3.7 or higher
- OpenCV (opencv-python >= 4.8.0)
- NumPy (>= 1.24.0)

**Installation**:

```bash
cd cv2
pip3 install -r requirements.txt
```

**Usage**:

```bash
python3 cv2/main.py [folder_path]
```

For more details, see [cv2/README.md](cv2/README.md).

### 5. imageio (Python + imageio)

Uses imageio library for image reading and NumPy for processing.

**Location**: `imageio/`

**Requirements**:

- Python 3.7 or higher
- imageio (>= 2.31.0)
- NumPy (>= 1.24.0)

**Installation**:

```bash
cd imageio
pip3 install -r requirements.txt
```

**Usage**:

```bash
python3 imageio/main.py [folder_path]
```

For more details, see [imageio/README.md](imageio/README.md).

## Benchmark Script

The repository includes a benchmark script that runs all five solutions 10 times each and compares their performance.

### Requirements

- Python 3.7 or higher
- All five solutions must be properly set up (see individual solution requirements above)

### Setup

1. **Install Python Dependencies** for all Python solutions:

```bash
# pillow
cd pillow && pip3 install -r requirements.txt && cd ..

# cv2
cd cv2 && pip3 install -r requirements.txt && cd ..

# imageio
cd imageio && pip3 install -r requirements.txt && cd ..
```

2. **Build Go Executables** (optional but recommended):

```bash
# govips
cd govips && go mod tidy && go build -o govips main.go && cd ..

# goimage
cd goimage && go build -o goimage main.go && cd ..
```

3. **Prepare Test Data**: Ensure the `data` folder exists and contains image files.

### Usage

Run the benchmark script from the project root:

```bash
python3 benchmark.py
```

Or make it executable and run directly:

```bash
chmod +x benchmark.py
./benchmark.py
```

### Output

The benchmark script will:

1. Run each solution 10 times
2. Display the full output from each run
3. Extract and display the internal analysis time for each run
4. Calculate and display statistics for each solution:
   - Average analysis time
   - Minimum analysis time
   - Maximum analysis time
5. Display a final comparison table sorted by average analysis time

### What is Measured

The benchmark extracts the **internal analysis time** reported by each solution, which is the time measured by `end_time - start_time` within each solution's code. This represents the actual image analysis time, not the total program execution time (which includes file I/O, program startup, etc.).

## Quick Start

1. **Clone the repository** (if applicable)

2. **Set up at least one solution**:

   - For Python solutions: `cd <solution_name> && pip3 install -r requirements.txt`
   - For Go solutions: `cd <solution_name> && go build -o <executable_name> main.go`

3. **Prepare test images** in the `data` folder

4. **Run a solution**:

   ```bash
   # Python solutions
   python3 <solution_name>/main.py

   # Go solutions
   cd <solution_name> && ./<executable_name>
   ```

5. **Run benchmarks** (after setting up all solutions):
   ```bash
   python3 benchmark.py
   ```

## Supported Image Formats

The supported formats vary by implementation:

- **cv2, imageio, pillow, govips**: JPG, JPEG, PNG, GIF, BMP, WEBP, TIFF
- **goimage**: JPG, JPEG, PNG, GIF (Go standard library limitations)

## Output Format

Each solution outputs results in the following format:

```
<filename> (<width>x<height>): <image_type>
...
Total processing time: X.XX milliseconds
```

**Example**:

```
150x150.jpg (150x150): Mixed pixels
all_black_1280x720.jpeg (1280x720): All black
all_white_300x250.jpg (300x250): All white
all_pink_500x500.jpeg (500x500): Single color (gray value: 128)
Total processing time: 15.23 milliseconds
```

## Functional Requirements

For detailed information about the image detection functionality, requirements, and specifications, please refer to [spec.md](spec.md).

## Notes

- All solutions use the `data` folder as the default image source
- Custom folder paths can be specified as command-line arguments
- The benchmark script expects all solutions to output "Total processing time: X.XX milliseconds"
- Go executables are optional; the benchmark script will fall back to `go run` if executables are not found
