# Image Format Converter

A simple Python script to convert images from one format to another using a GUI file picker. Supports JPEG, PNG, HEIC, and other major image formats. Compatible with both macOS and Windows.

## Features
- Select one or more images via a native file picker (Finder or File Explorer).
- Choose output format from a list of supported types.
- Converts and saves images in the chosen format in the same directory.

## Supported Formats
- JPEG (.jpg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)
- WEBP (.webp)
- HEIC (.heic)
- GIF (.gif)

## Requirements
- Python 3.7+
- Pillow
- pillow-heif (for HEIC format)

## Installation
1. Clone this repo or download the script.
2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage
Run the script using Python:
```bash
python image_converter_tool.py
```
1. A file picker will appear. Select one or more image files.
2. Input the desired output format when prompted.
3. Converted images will be saved in the same directory as the originals.

## Notes
- The script automatically appends the correct file extension.
- If an unsupported format is typed, the script will exit with an error message.

## License
MIT
