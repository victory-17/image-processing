import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import numpy as np
from Segmentation import (manual_threshold, histogram_peak_threshold, 
                          histogram_valley_threshold, adaptive_histogram_threshold, 
                          calculate_threshold)

class SegmentationGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Histogram-Based Segmentation")

        self.canvas = tk.Canvas(master, width=400, height=400, bg='gray')
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        self.controls = tk.Frame(master)
        self.controls.pack(side=tk.RIGHT, padx=10, pady=10)

        # Buttons
        self.upload_btn = tk.Button(self.controls, text="+ Upload Image", bg="green", fg="white", command=self.upload_image)
        self.upload_btn.pack(pady=5)

        self.manual_btn = tk.Button(self.controls, text="Manual Threshold", command=self.apply_manual_threshold, state=tk.DISABLED)
        self.manual_btn.pack(pady=5)

        self.peak_btn = tk.Button(self.controls, text="Histogram Peak Threshold", command=self.apply_peak_threshold, state=tk.DISABLED)
        self.peak_btn.pack(pady=5)

        self.valley_btn = tk.Button(self.controls, text="Histogram Valley Threshold", command=self.apply_valley_threshold, state=tk.DISABLED)
        self.valley_btn.pack(pady=5)

        self.adaptive_btn = tk.Button(self.controls, text="Adaptive Histogram Threshold", command=self.apply_adaptive_threshold, state=tk.DISABLED)
        self.adaptive_btn.pack(pady=5)

        self.reset_btn = tk.Button(self.controls, text="Reset to Original", bg="#000080", fg="white", command=self.reset_image, state=tk.DISABLED)
        self.reset_btn.pack(pady=5)

        self.calculate_threshold_btn = tk.Button(self.controls, text="Calculate Threshold", command=self.calculate_threshold, state=tk.DISABLED)
        self.calculate_threshold_btn.pack(pady=5)

        self.threshold_label = tk.Label(self.controls, text="Threshold: N/A", font=("Arial", 12))
        self.threshold_label.pack(pady=5)

        self.image = None
        self.original_image = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((400, 400))
            self.image = img
            self.original_image = img.copy()
            self.display_image(img)
            self.manual_btn.config(state=tk.NORMAL)
            self.peak_btn.config(state=tk.NORMAL)
            self.valley_btn.config(state=tk.NORMAL)
            self.adaptive_btn.config(state=tk.NORMAL)
            self.reset_btn.config(state=tk.NORMAL)
            self.calculate_threshold_btn.config(state=tk.NORMAL)

    def display_image(self, img):
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.image = img_tk
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

    def apply_manual_threshold(self):
        if self.image:
            threshold_image = manual_threshold(self.image, threshold=128)  # 128 as example threshold
            self.display_image(threshold_image)

    def apply_peak_threshold(self):
        if self.image:
            peak_threshold_image = histogram_peak_threshold(self.image)
            self.display_image(peak_threshold_image)

    def apply_valley_threshold(self):
        if self.image:
            valley_threshold_image = histogram_valley_threshold(self.image)
            self.display_image(valley_threshold_image)

    def apply_adaptive_threshold(self):
        if self.image:
            adaptive_threshold_image = adaptive_histogram_threshold(self.image)
            self.display_image(adaptive_threshold_image)

    def reset_image(self):
        if self.original_image:
            self.image = self.original_image.copy()
            self.display_image(self.image)

    def calculate_threshold(self):
        if self.image:
            threshold = calculate_threshold(self.image)
            self.threshold_label.config(text=f"Threshold: {threshold:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SegmentationGUI(root)
    root.mainloop()
