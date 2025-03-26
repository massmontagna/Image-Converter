import os
import sys
import tkinter
from PIL import Image
from tkinter import Tk, filedialog, simpledialog, messagebox
from pathlib import Path
import pillow_heif

# Register HEIF plugin
pillow_heif.register_heif_opener()

# Supported formats
SUPPORTED_FORMATS = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "BMP": ".bmp",
    "TIFF": ".tiff",
    "WEBP": ".webp",
    "HEIC": ".heic",
    "GIF": ".gif"
}

def choose_files():
    root = Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title="Select Image Files",
        filetypes=[("Image files", ["*" + ext for ext in SUPPORTED_FORMATS.values()])]
    )
    return list(file_paths)

def ask_output_format():
    root = Tk()
    root.withdraw()
    formats = list(SUPPORTED_FORMATS.keys())
    selected_format = simpledialog.askstring(
        "Select Output Format",
        f"Choose output format from: {', '.join(formats)}"
    )
    if selected_format and selected_format.upper() in SUPPORTED_FORMATS:
        return selected_format.upper()
    else:
        messagebox.showerror("Error", "Invalid format selected.")
        sys.exit(1)

def convert_images(file_paths, output_format):
    output_ext = SUPPORTED_FORMATS[output_format]
    for file_path in file_paths:
        try:
            img = Image.open(file_path)
            output_file = Path(file_path).with_suffix(output_ext)
            img.save(output_file, output_format)
            print(f"Converted {file_path} -> {output_file}")
        except Exception as e:
            print(f"Failed to convert {file_path}: {e}")

def main():
    files = choose_files()
    if not files:
        print("No files selected.")
        return

    output_format = ask_output_format()
    convert_images(files, output_format)

if __name__ == "__main__":
    main()
