# Image Detection Tool (Go + standard image)

## Requirements

- Go 1.21 or higher

## Installation

No external dependencies required. This implementation uses only Go standard library packages.

## Usage

Process all images in the `data` folder (default):

```bash
go run main.go
```

Or build and run:

```bash
go build -o goimage main.go
./goimage
```

Process images from a custom folder:

```bash
go run main.go /path/to/image/folder
```

**Note:** Go standard library supports JPEG, PNG, and GIF formats only. BMP, WEBP, and TIFF formats are not supported by the standard library.
