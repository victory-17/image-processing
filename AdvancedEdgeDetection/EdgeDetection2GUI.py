import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
from EdgeDetection2 import homogeneity_operator, difference_operator, variance_operator, range_operator
import numpy as np

class EdgeDetectionGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced Edge Detection")

        self.canvas = tk.Canvas(master, width=400, height=400, bg='gray')
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        self.controls = tk.Frame(master)
        self.controls.pack(side=tk.RIGHT, padx=10, pady=10)

        # Buttons
        self.upload_btn = tk.Button(self.controls, text="+ Upload Image", bg="green", fg="white", command=self.upload_image)
        self.upload_btn.pack(pady=5)

        self.grayscale_btn = tk.Button(self.controls, text="Convert to Grayscale", bg="darkgray", fg="white", command=self.convert_to_grayscale, state=tk.DISABLED)
        self.grayscale_btn.pack(pady=5)

        self.homogeneity_btn = tk.Button(self.controls, text="Homogeneity Operator", command=self.apply_homogeneity, state=tk.DISABLED)
        self.homogeneity_btn.pack(pady=5)

        self.difference_btn = tk.Button(self.controls, text="Difference Operator", command=self.apply_difference, state=tk.DISABLED)
        self.difference_btn.pack(pady=5)

        self.variance_btn = tk.Button(self.controls, text="Variance Operator", command=self.apply_variance, state=tk.DISABLED)
        self.variance_btn.pack(pady=5)

        self.range_btn = tk.Button(self.controls, text="Range Operator", command=self.apply_range, state=tk.DISABLED)
        self.range_btn.pack(pady=5)

        self.threshold_btn = tk.Button(self.controls, text="Calculate Threshold", command=self.calculate_threshold, state=tk.DISABLED)
        self.threshold_btn.pack(pady=5)

        self.reset_btn = tk.Button(self.controls, text="Reset to Original", bg="#000080", fg="white", command=self.reset_to_original, state=tk.DISABLED)
        self.reset_btn.pack(pady=5)

        self.threshold_label = tk.Label(self.controls, text="Threshold: N/A", font=("Arial", 12))
        self.threshold_label.pack(pady=5)

        self.image = None
        self.gray_image = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((400, 400))
            self.image = img
            self.display_image(img)
            self.grayscale_btn.config(state=tk.NORMAL)
            self.reset_btn.config(state=tk.NORMAL)  # Enable reset button after upload

    def display_image(self, img):
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.image = img_tk
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

    def convert_to_grayscale(self):
        if self.image:
            gray = ImageOps.grayscale(self.image)
            self.gray_image = gray
            self.display_image(gray)
            self.homogeneity_btn.config(state=tk.NORMAL)
            self.difference_btn.config(state=tk.NORMAL)
            self.variance_btn.config(state=tk.NORMAL)
            self.range_btn.config(state=tk.NORMAL)
            self.threshold_btn.config(state=tk.NORMAL)

    def apply_homogeneity(self):
        if self.gray_image:
            homogeneity = homogeneity_operator(self.gray_image)
            self.display_image(homogeneity)

    def apply_difference(self):
        if self.gray_image:
            difference = difference_operator(self.gray_image)
            self.display_image(difference)

    def apply_variance(self):
        if self.gray_image:
            variance = variance_operator(self.gray_image)
            self.display_image(variance)

    def apply_range(self):
        if self.gray_image:
            range_image = range_operator(self.gray_image)
            self.display_image(range_image)

    def calculate_threshold(self):
        if self.gray_image:
            np_image = np.array(self.gray_image)
            threshold = np.mean(np_image)
            optimal = "Optimal" if threshold > 127 else "Not Optimal"
            self.threshold_label.config(text=f"Threshold: {threshold:.2f} ({optimal})")

    def reset_to_original(self):
        if self.image:
            self.display_image(self.image)
            self.gray_image = None
            # Disable operator buttons when resetting
            self.homogeneity_btn.config(state=tk.DISABLED)
            self.difference_btn.config(state=tk.DISABLED)
            self.variance_btn.config(state=tk.DISABLED)
            self.range_btn.config(state=tk.DISABLED)
            self.threshold_btn.config(state=tk.DISABLED)
            self.threshold_label.config(text="Threshold: N/A")

if __name__ == "__main__":
    root = tk.Tk()
    app = EdgeDetectionGUI(root)
    root.mainloop()
