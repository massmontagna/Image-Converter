import os
import sys
from PIL import Image
from tkinter import Tk, filedialog, messagebox, StringVar, IntVar, BooleanVar
from tkinter.ttk import Combobox, Button, Label, Entry, Frame, Checkbutton
from pathlib import Path
import pillow_heif

# Register HEIF plugin
pillow_heif.register_heif_opener()

SUPPORTED_FORMATS = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "BMP": ".bmp",
    "TIFF": ".tiff",
    "WEBP": ".webp",
    "HEIC": ".heic",
    "GIF": ".gif"
}

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Format Converter")
        self.root.geometry("400x350")

        self.file_paths = []
        self.output_format = StringVar(value="JPEG")
        self.width = IntVar(value=0)
        self.height = IntVar(value=0)
        self.lock_aspect_ratio = BooleanVar(value=False)

        self.setup_ui()

    def setup_ui(self):
        Label(self.root, text="Select Images:").pack(pady=5)
        Button(self.root, text="Browse", command=self.choose_files).pack()

        Label(self.root, text="Output Format:").pack(pady=5)
        Combobox(self.root, textvariable=self.output_format, values=list(SUPPORTED_FORMATS.keys()), state="readonly").pack()

        Label(self.root, text="Resize Options (0 = keep original):").pack(pady=10)

        resize_frame = Frame(self.root)
        resize_frame.pack()
        Label(resize_frame, text="Width:").grid(row=0, column=0)
        Entry(resize_frame, textvariable=self.width, width=10).grid(row=0, column=1)
        Label(resize_frame, text="Height:").grid(row=0, column=2)
        Entry(resize_frame, textvariable=self.height, width=10).grid(row=0, column=3)

        Checkbutton(self.root, text="Lock Aspect Ratio", variable=self.lock_aspect_ratio).pack(pady=5)

        Button(self.root, text="Convert Images", command=self.convert_images).pack(pady=20)

    def choose_files(self):
        self.file_paths = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[("Image files", ["*" + ext for ext in SUPPORTED_FORMATS.values()])]
        )

    def convert_images(self):
        if not self.file_paths:
            messagebox.showerror("Error", "No files selected.")
            return

        output_format = self.output_format.get()
        output_ext = SUPPORTED_FORMATS[output_format]
        target_width = self.width.get()
        target_height = self.height.get()
        lock_aspect = self.lock_aspect_ratio.get()

        for file_path in self.file_paths:
            try:
                img = Image.open(file_path)
                orig_width, orig_height = img.size

                if target_width > 0 and target_height > 0:
                    if lock_aspect:
                        aspect_ratio = orig_width / orig_height
                        if target_width / target_height > aspect_ratio:
                            target_width = int(target_height * aspect_ratio)
                        else:
                            target_height = int(target_width / aspect_ratio)
                    img = img.resize((target_width, target_height), Image.LANCZOS)

                output_file = Path(file_path).with_suffix(output_ext)
                img.save(output_file, output_format)
                print(f"Converted {file_path} -> {output_file}")

            except Exception as e:
                print(f"Failed to convert {file_path}: {e}")

        messagebox.showinfo("Done", "Image conversion completed!")


def main():
    root = Tk()
    app = ImageConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
