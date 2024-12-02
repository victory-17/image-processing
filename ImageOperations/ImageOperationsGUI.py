import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import numpy as np
from ImageOperations import add_images, subtract_images, invert_image

class ImageOperationsGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Operations")

        self.canvas = tk.Canvas(master, width=400, height=400, bg='gray')
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        self.controls = tk.Frame(master)
        self.controls.pack(side=tk.RIGHT, padx=10, pady=10)

        # Buttons
        self.upload_btn = tk.Button(self.controls, text="+ Upload Image", bg="green", fg="white", command=self.upload_image)
        self.upload_btn.pack(pady=5)

        self.add_btn = tk.Button(self.controls, text="Add Image to Copy", command=self.add_image, state=tk.DISABLED)
        self.add_btn.pack(pady=5)

        self.subtract_btn = tk.Button(self.controls, text="Subtract Image from Copy", command=self.subtract_image, state=tk.DISABLED)
        self.subtract_btn.pack(pady=5)

        self.invert_btn = tk.Button(self.controls, text="Invert Image", command=self.invert_image, state=tk.DISABLED)
        self.invert_btn.pack(pady=5)

        self.reset_btn = tk.Button(self.controls, text="Reset to Original", bg="#000080", fg="white", command=self.reset_image, state=tk.DISABLED)
        self.reset_btn.pack(pady=5)

        self.threshold_btn = tk.Button(self.controls, text="Calculate Threshold", command=self.calculate_threshold, state=tk.DISABLED)
        self.threshold_btn.pack(pady=5)

        self.threshold_label = tk.Label(self.controls, text="Threshold: N/A", font=("Arial", 12))
        self.threshold_label.pack(pady=5)

        self.image = None
        self.original_image = None
        self.gray_image = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((400, 400))
            self.image = img
            self.original_image = img.copy()
            self.display_image(img)
            self.add_btn.config(state=tk.NORMAL)
            self.subtract_btn.config(state=tk.NORMAL)
            self.invert_btn.config(state=tk.NORMAL)
            self.reset_btn.config(state=tk.NORMAL)
            self.threshold_btn.config(state=tk.NORMAL)

    def display_image(self, img):
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.image = img_tk
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

    def add_image(self):
        if self.image:
            added_image = add_images(self.image)
            self.display_image(added_image)

    def subtract_image(self):
        if self.image:
            subtracted_image = subtract_images(self.image)
            self.display_image(subtracted_image)

    def invert_image(self):
        if self.image:
            inverted_image = invert_image(self.image)
            self.display_image(inverted_image)

    def reset_image(self):
        if self.original_image:
            self.image = self.original_image.copy()
            self.display_image(self.image)

    def calculate_threshold(self):
        if self.image:
            np_image = np.array(self.image)
            threshold = np.mean(np_image)
            optimal = "Optimal" if threshold > 127 else "Not Optimal"
            self.threshold_label.config(text=f"Threshold: {threshold:.2f} ({optimal})")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageOperationsGUI(root)
    root.mainloop()
