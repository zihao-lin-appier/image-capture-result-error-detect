# govips Project

This project uses the govips library to detect whether an image is all black, all white, or has mixed pixels.

## Requirements

1. **Go** (version 1.21 or higher)

   - Installation: Visit https://golang.org/dl/ to download and install
   - Or use Homebrew: `brew install go`

2. **libvips** (system dependency)
   - macOS: `brew install vips`
   - Linux: `sudo apt-get install libvips-dev` (Ubuntu/Debian) or `sudo yum install vips-devel` (CentOS/RHEL)
   - Windows: Download precompiled binaries

## Installation Steps

1. Install Go and libvips (if not already installed)

2. Install Go dependencies:

```bash
cd govips
go mod tidy
```

3. Prepare test image:

   - Name the test image `test.png` and place it in the `govips` directory
   - Or modify the file path in `main.go`

4. Run the program:

```bash
go run main.go
```

## Build

```bash
go build -o govips main.go
./govips
```

## Code Explanation

The code performs the following steps to detect image type:

1. **Load Image**: Loads the image from file using `NewImageFromFile()`
2. **Convert to Grayscale**: If the image has multiple color channels, it converts to grayscale using `ToColorSpace(InterpretationBW)`
3. **Cast to uint8**: Ensures the image is in uint8 format using `Cast(BandFormatUchar)` for proper byte extraction
4. **Extract Pixel Data**: Uses `ToBytes()` to get raw pixel data as bytes
5. **Calculate Statistics**: Finds the minimum and maximum pixel values
6. **Determine Type**:
   - If min == 0 and max == 0: "All black"
   - If min == 255 and max == 255: "All white"
   - Otherwise: "Mixed pixels"

## Dependencies

- **govips/v2**: v2.16.0 (latest stable version)
- **Go**: 1.21 or higher
