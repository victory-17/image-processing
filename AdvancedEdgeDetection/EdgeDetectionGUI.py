import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
from EdgeDetection import contrast_based_edge, difference_of_gaussians
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

        self.contrast_btn = tk.Button(self.controls, text="Contrast-Based Edge", command=self.apply_contrast_based_edge, state=tk.DISABLED)
        self.contrast_btn.pack(pady=5)

        self.dog_7x7_btn = tk.Button(self.controls, text="Difference of Gaussians (7x7)", command=self.apply_dog_7x7, state=tk.DISABLED)
        self.dog_7x7_btn.pack(pady=5)

        self.dog_9x9_btn = tk.Button(self.controls, text="Difference of Gaussians (9x9)", command=self.apply_dog_9x9, state=tk.DISABLED)
        self.dog_9x9_btn.pack(pady=5)

        self.dog_btn = tk.Button(self.controls, text="Difference of Gaussians", command=self.apply_dog)
        self.dog_btn.pack(pady=5)

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
            self.reset_btn.config(state=tk.NORMAL)

    def display_image(self, img):
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.image = img_tk
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

    def convert_to_grayscale(self):
        if self.image:
            gray = ImageOps.grayscale(self.image)
            self.gray_image = gray
            self.display_image(gray)
            self.contrast_btn.config(state=tk.NORMAL)
            self.dog_7x7_btn.config(state=tk.NORMAL)
            self.dog_9x9_btn.config(state=tk.NORMAL)
            self.threshold_btn.config(state=tk.NORMAL)

    def apply_contrast_based_edge(self):
        if self.gray_image:
            contrast_edge = contrast_based_edge(self.gray_image)
            self.display_image(contrast_edge)

    def apply_dog_7x7(self):
        if self.gray_image:
            dog_7x7, dog_9x9, dog = difference_of_gaussians(self.gray_image)
            self.display_image(dog_7x7)

    def apply_dog_9x9(self):
        if self.gray_image:
            dog_7x7, dog_9x9, dog = difference_of_gaussians(self.gray_image)
            self.display_image(dog_9x9)

    def apply_dog(self):
        if self.gray_image:
            dog_7x7, dog_9x9, dog = difference_of_gaussians(self.gray_image)
            self.display_image(dog)

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
            self.contrast_btn.config(state=tk.DISABLED)
            self.dog_7x7_btn.config(state=tk.DISABLED)
            self.dog_9x9_btn.config(state=tk.DISABLED)
            self.threshold_btn.config(state=tk.DISABLED)
            self.threshold_label.config(text="Threshold: N/A")

if __name__ == "__main__":
    root = tk.Tk()
    app = EdgeDetectionGUI(root)
    root.mainloop()
