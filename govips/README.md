# Image Detection Tool (Go + govips)

## Requirements

1. **Go** (version 1.21 or higher)

   - Installation: Visit https://golang.org/dl/ to download and install
   - Or use Homebrew: `brew install go`

2. **libvips** (system dependency)
   - macOS: `brew install vips`
   - Linux: `sudo apt-get install libvips-dev` (Ubuntu/Debian) or `sudo yum install vips-devel` (CentOS/RHEL)
   - Windows: Download precompiled binaries

## Installation

1. Install Go and libvips (if not already installed)

2. Install Go dependencies:

```bash
cd govips
go mod tidy
```

## Usage

Run the program:

```bash
go run main.go
```

Or build and run:

```bash
go build -o govips main.go
./govips
```
