package main

import (
	"fmt"
	"image"
	_ "image/gif"
	_ "image/jpeg"
	_ "image/png"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"time"
)

// Supported image formats (formats supported by Go standard library)
var supportedExts = map[string]bool{
	".jpg":  true,
	".jpeg": true,
	".png":  true,
	".gif":  true,
}

type ImageInfo struct {
	Type   string
	Width  int
	Height int
}

// calculateGrayValue calculates the gray value (brightness) of an RGB color.
// Uses the standard luminance formula: 0.299*R + 0.587*G + 0.114*B
func calculateGrayValue(r, g, b uint32) int {
	return int(0.299*float64(r>>8) + 0.587*float64(g>>8) + 0.114*float64(b>>8))
}

// normalizeGrayValue normalizes gray value to range 1-254 for single color images.
func normalizeGrayValue(grayValue int) int {
	if grayValue == 0 {
		return 1
	}
	if grayValue == 255 {
		return 254
	}
	return grayValue
}

// detectImageType detects the type of an image.
func detectImageType(img image.Image) string {
	bounds := img.Bounds()
	width := bounds.Dx()
	height := bounds.Dy()

	if width == 0 || height == 0 {
		return "Mixed pixels"
	}

	// Get the first pixel as reference
	firstPixel := img.At(bounds.Min.X, bounds.Min.Y)
	firstR, firstG, firstB, _ := firstPixel.RGBA()
	firstGray := calculateGrayValue(firstR, firstG, firstB)

	// Check if all pixels are the same
	allSame := true
	allSameGray := true

	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			pixel := img.At(x, y)
			r, g, b, _ := pixel.RGBA()

			// Check if pixel is identical to first pixel
			if r != firstR || g != firstG || b != firstB {
				allSame = false
			}

			// Check if pixel has same gray value
			gray := calculateGrayValue(r, g, b)
			if gray != firstGray {
				allSameGray = false
			}

			// Early exit if we found different pixels
			if !allSame && !allSameGray {
				return "Mixed pixels"
			}
		}
	}

	if allSame {
		// All pixels are identical
		r8 := firstR >> 8
		g8 := firstG >> 8
		b8 := firstB >> 8

		if r8 == 0 && g8 == 0 && b8 == 0 {
			return "All black"
		}
		if r8 == 255 && g8 == 255 && b8 == 255 {
			return "All white"
		}
		// Single color (not black or white)
		return fmt.Sprintf("Single color (gray value: %d)", normalizeGrayValue(firstGray))
	}

	if allSameGray {
		// All pixels have the same brightness but different colors
		return fmt.Sprintf("Single color (gray value: %d)", normalizeGrayValue(firstGray))
	}

	return "Mixed pixels"
}

// processImage processes a single image and returns its information.
func processImage(imagePath string) (*ImageInfo, error) {
	file, err := os.Open(imagePath)
	if err != nil {
		return nil, fmt.Errorf("error opening file: %v", err)
	}
	defer file.Close()

	img, _, err := image.Decode(file)
	if err != nil {
		return nil, fmt.Errorf("error decoding image: %v", err)
	}

	bounds := img.Bounds()
	width := bounds.Dx()
	height := bounds.Dy()
	imageType := detectImageType(img)

	return &ImageInfo{
		Type:   imageType,
		Width:  width,
		Height: height,
	}, nil
}

// getImageFiles gets all image files from the specified folder.
func getImageFiles(folderPath string) ([]string, error) {
	entries, err := os.ReadDir(folderPath)
	if err != nil {
		return nil, fmt.Errorf("error reading directory: %v", err)
	}

	var imageFiles []string
	for _, entry := range entries {
		if !entry.IsDir() {
			ext := strings.ToLower(filepath.Ext(entry.Name()))
			if supportedExts[ext] {
				imageFiles = append(imageFiles, filepath.Join(folderPath, entry.Name()))
			}
		}
	}

	sort.Strings(imageFiles)
	return imageFiles, nil
}

// processImages processes all images in the specified folder.
func processImages(folderPath string) error {
	imageFiles, err := getImageFiles(folderPath)
	if err != nil {
		return err
	}

	if len(imageFiles) == 0 {
		fmt.Printf("No supported image files found in '%s'.\n", folderPath)
		fmt.Printf("Supported formats: %s\n", strings.Join([]string{".jpg", ".jpeg", ".png", ".gif"}, ", "))
		return nil
	}

	// Record start time
	startTime := time.Now()

	// Process each image
	for _, imagePath := range imageFiles {
		info, err := processImage(imagePath)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error processing %s: %v\n", filepath.Base(imagePath), err)
			continue
		}
		fmt.Printf("%s (%dx%d): %s\n", filepath.Base(imagePath), info.Width, info.Height, info.Type)
	}

	// Calculate and print elapsed time
	elapsed := time.Since(startTime)
	fmt.Printf("Total processing time: %.2f milliseconds\n", float64(elapsed.Nanoseconds())/1e6)

	return nil
}

func main() {
	// Get the default data folder path (project root/data)
	// Use current working directory as base, then go up one level to find data folder
	wd, err := os.Getwd()
	if err != nil {
		wd = "."
	}
	
	// If we're in goimage folder, go up one level to find data
	scriptDir := filepath.Base(wd)
	var defaultDataPath string
	if scriptDir == "goimage" {
		defaultDataPath = filepath.Join(wd, "..", "data")
	} else {
		// Assume we're in project root
		defaultDataPath = filepath.Join(wd, "data")
	}

	dataDir := defaultDataPath
	if len(os.Args) > 1 {
		dataDir = os.Args[1]
	}

	// Resolve absolute path
	absPath, err := filepath.Abs(dataDir)
	if err != nil {
		fmt.Printf("Error resolving path: %v\n", err)
		os.Exit(1)
	}

	if err := processImages(absPath); err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
}

