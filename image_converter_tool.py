import os
import sys
from PIL import Image, ImageTk
from tkinter import Tk, filedialog, messagebox, StringVar, IntVar, BooleanVar
from tkinter.ttk import Combobox, Button, Label, Entry, Frame, Checkbutton
from pathlib import Path
import pillow_heif
from tkinterdnd2 import DND_FILES, TkinterDnD

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
        self.root.geometry("800x400")

        self.file_paths = []
        self.output_format = StringVar(value="JPEG")
        self.width = IntVar(value=0)
        self.height = IntVar(value=0)
        self.lock_aspect_ratio = BooleanVar(value=False)
        self.orig_aspect_ratio = None
        self.preview_index = 0

        self.setup_ui()
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

    def setup_ui(self):
        Label(self.root, text="Select Images:").pack(pady=5)
        Button(self.root, text="Browse", command=self.choose_files).pack()

        Label(self.root, text="Output Format:").pack(pady=5)
        Combobox(self.root, textvariable=self.output_format, values=list(SUPPORTED_FORMATS.keys()), state="readonly").pack()

        Label(self.root, text="Resize Options (0 = keep original):").pack(pady=10)

        resize_frame = Frame(self.root)
        resize_frame.pack()
        Label(resize_frame, text="Width:").grid(row=0, column=0)
        self.width_entry = Entry(resize_frame, textvariable=self.width, width=10)
        self.width_entry.grid(row=0, column=1)
        self.width_entry.bind("<KeyRelease>", self.update_height_based_on_aspect)
        Label(resize_frame, text="Height:").grid(row=0, column=2)
        self.height_entry = Entry(resize_frame, textvariable=self.height, width=10)
        self.height_entry.grid(row=0, column=3)
        self.height_entry.bind("<KeyRelease>", self.update_width_based_on_aspect)

        Checkbutton(self.root, text="Lock Aspect Ratio", variable=self.lock_aspect_ratio).pack(pady=5)

        Button(self.root, text="Convert Images", command=self.convert_images).pack(pady=20)

        preview_frame = Frame(self.root)
        preview_frame.pack(pady=10)

        original_frame = Frame(preview_frame)
        original_frame.pack(side="left", padx=10)
        Label(original_frame, text="Original").pack()
        self.preview_label = Label(original_frame)
        self.preview_label.pack()

        resized_frame = Frame(preview_frame)
        resized_frame.pack(side="left", padx=10)
        Label(resized_frame, text="Resized").pack()
        self.output_preview_label = Label(resized_frame)
        self.output_preview_label.pack()

        self.info_label = Label(self.root, text="")
        self.info_label.pack(pady=5)

        btn_frame = Frame(self.root)
        btn_frame.pack()
        Button(btn_frame, text="Previous", command=self.show_previous_preview).pack(side="left", padx=5)
        Button(btn_frame, text="Next", command=self.show_next_preview).pack(side="left", padx=5)

    def choose_files(self):
        self.file_paths = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[("Image files", ["*" + ext for ext in SUPPORTED_FORMATS.values()])]
        )
        if self.file_paths:
            self.preview_index = 0
            self.show_preview(self.preview_index)

    def show_preview(self, index):
        if not self.file_paths:
            return
        try:
            img = Image.open(self.file_paths[index])
            self.orig_aspect_ratio = img.width / img.height
            img.thumbnail((300, 300))
            img_tk = ImageTk.PhotoImage(img)
            self.preview_label.configure(image=img_tk)
            self.preview_label.image = img_tk

            output_img = img.copy()
            target_width = self.width.get()
            target_height = self.height.get()
            if target_width > 0 and target_height > 0:
                output_img = output_img.resize((target_width, target_height), Image.LANCZOS)
            output_img.thumbnail((300, 300))
            output_img_tk = ImageTk.PhotoImage(output_img)
            self.output_preview_label.configure(image=output_img_tk)
            self.output_preview_label.image = output_img_tk

            file_size_kb = os.path.getsize(self.file_paths[index]) / 1024
            self.info_label.config(text=f"{img.width}x{img.height}px | {file_size_kb:.1f} KB")
        except Exception as e:
            print(f"Error showing preview: {e}")

    def show_next_preview(self):
        if self.preview_index < len(self.file_paths) - 1:
            self.preview_index += 1
            self.show_preview(self.preview_index)

    def show_previous_preview(self):
        if self.preview_index > 0:
            self.preview_index -= 1
            self.show_preview(self.preview_index)

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

    def update_height_based_on_aspect(self, event):
        if self.lock_aspect_ratio.get() and self.orig_aspect_ratio:
            try:
                w = int(self.width.get())
                h = int(w / self.orig_aspect_ratio)
                self.height.set(h)
            except Exception:
                pass
        self.show_preview(self.preview_index)

    def update_width_based_on_aspect(self, event):
        if self.lock_aspect_ratio.get() and self.orig_aspect_ratio:
            try:
                h = int(self.height.get())
                w = int(h * self.orig_aspect_ratio)
                self.width.set(w)
            except Exception:
                pass
        self.show_preview(self.preview_index)

    def on_drop(self, event):
        self.file_paths = self.root.tk.splitlist(event.data)
        if self.file_paths:
            self.preview_index = 0
            self.show_preview(self.preview_index)

def main():
    root = TkinterDnD.Tk()
    app = ImageConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
