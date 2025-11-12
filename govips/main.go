package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/davidbyttow/govips/v2/vips"
)

type ImageInfo struct {
	Type   string
	Width  int
	Height int
}

func detectImageType(filePath string) (*ImageInfo, error) {
	img, err := vips.NewImageFromFile(filePath)
	if err != nil {
		return nil, fmt.Errorf("error loading image: %v", err)
	}
	defer img.Close()

	// Get image dimensions
	width := img.Width()
	height := img.Height()

	// Convert to grayscale if needed
	if img.Bands() > 1 {
		if err := img.ToColorSpace(vips.InterpretationBW); err != nil {
			return nil, fmt.Errorf("error converting to grayscale: %v", err)
		}
	}

	// Ensure image is in uint8 format for ToBytes()
	if err := img.Cast(vips.BandFormatUchar); err != nil {
		return nil, fmt.Errorf("error casting image format: %v", err)
	}

	// Get pixel data as bytes
	data, err := img.ToBytes()
	if err != nil {
		return nil, fmt.Errorf("error getting pixel data: %v", err)
	}

	if len(data) == 0 {
		return nil, fmt.Errorf("image has no pixel data")
	}

	// Calculate min and max
	min := uint8(255)
	max := uint8(0)
	for _, b := range data {
		if b < min {
			min = b
		}
		if b > max {
			max = b
		}
	}

	// Determine image type based on pixel values
	var result string
	if min == 0 && max == 0 {
		result = "All black"
	} else if min == 255 && max == 255 {
		result = "All white"
	} else if min == max {
		// All pixels have the same value (but not 0 or 255)
		result = fmt.Sprintf("Single color (gray value: %d)", min)
	} else {
		result = "Mixed pixels"
	}

	return &ImageInfo{
		Type:   result,
		Width:  width,
		Height: height,
	}, nil
}

func main() {
	vips.Startup(nil)
	defer vips.Shutdown()

	dataDir := "../data"
	if len(os.Args) > 1 {
		dataDir = os.Args[1]
	}

	// Read all files in the data directory
	entries, err := os.ReadDir(dataDir)
	if err != nil {
		fmt.Printf("Error reading directory %s: %v\n", dataDir, err)
		os.Exit(1)
	}

	// Supported image extensions
	imageExts := map[string]bool{
		".jpg":  true,
		".jpeg": true,
		".png":  true,
		".gif":  true,
		".bmp":  true,
		".webp": true,
		".tiff": true,
		".tif":  true,
	}

	var imageFiles []string
	for _, entry := range entries {
		if !entry.IsDir() {
			ext := strings.ToLower(filepath.Ext(entry.Name()))
			if imageExts[ext] {
				imageFiles = append(imageFiles, filepath.Join(dataDir, entry.Name()))
			}
		}
	}

	if len(imageFiles) == 0 {
		fmt.Printf("No image files found in %s\n", dataDir)
		os.Exit(1)
	}

	// Process each image file
	fmt.Printf("Processing %d image file(s) from %s:\n\n", len(imageFiles), dataDir)
	for _, filePath := range imageFiles {
		info, err := detectImageType(filePath)
		if err != nil {
			fmt.Printf("%s: ERROR - %v\n", filepath.Base(filePath), err)
		} else {
			fmt.Printf("%s (%dx%d): %s\n", filepath.Base(filePath), info.Width, info.Height, info.Type)
		}
	}
}

