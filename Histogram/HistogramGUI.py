import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
from Histogram import compute_histogram, histogram_equalization
import matplotlib.pyplot as plt
import numpy as np

class HistogramGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Histogram Operations")
        
        self.canvas = tk.Canvas(master, width=400, height=400, bg='gray')
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.controls = tk.Frame(master)
        self.controls.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Buttons
        self.upload_btn = tk.Button(self.controls, text="+ Upload Image", bg="green", fg="white", command=self.upload_image)
        self.upload_btn.pack(pady=5)
        
        self.grayscale_btn = tk.Button(self.controls, text="Convert to Grayscale", bg="darkgray", fg="white", command=self.convert_to_grayscale, state=tk.DISABLED)
        self.grayscale_btn.pack(pady=5)
        
        self.histogram_btn = tk.Button(self.controls, text="Show Histogram", command=self.show_histogram, state=tk.DISABLED)
        self.histogram_btn.pack(pady=5)
        
        self.equalize_btn = tk.Button(self.controls, text="Equalize Histogram", command=self.equalize_histogram, state=tk.DISABLED)
        self.equalize_btn.pack(pady=5)
        
        self.equalized_histogram_btn = tk.Button(self.controls, text="Show Equalized Histogram", command=self.show_equalized_histogram, state=tk.DISABLED)
        self.equalized_histogram_btn.pack(pady=5)
        
        self.analyze_histogram_btn = tk.Button(self.controls, text="Analyze Histogram", command=self.analyze_histogram, state=tk.DISABLED)
        self.analyze_histogram_btn.pack(pady=5)
        
        self.threshold_btn = tk.Button(self.controls, text="Calculate Threshold", command=self.calculate_threshold, state=tk.DISABLED)
        self.threshold_btn.pack(pady=5)
        
        self.threshold_label = tk.Label(self.controls, text="Threshold: N/A", font=("Arial", 12))
        self.threshold_label.pack(pady=5)
        
        self.analysis_label = tk.Label(self.controls, text="", font=("Arial", 10), wraplength=200)
        self.analysis_label.pack(pady=5)
        
        self.reset_btn = tk.Button(self.controls, text="Reset to Original", bg="#000080", fg="white", command=self.reset_to_original, state=tk.DISABLED)
        self.reset_btn.pack(pady=5)
        
        self.image = None
        self.gray_image = None
        self.equalized_image = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((400, 400))
            self.image = img
            self.display_image(img)
            self.grayscale_btn.config(state=tk.NORMAL)
            self.threshold_btn.config(state=tk.NORMAL)
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
            self.histogram_btn.config(state=tk.NORMAL)
            self.equalize_btn.config(state=tk.NORMAL)
            self.analyze_histogram_btn.config(state=tk.NORMAL)

    def calculate_threshold(self):
        if self.gray_image:
            np_image = np.array(self.gray_image)
            threshold = np.mean(np_image)
            optimal = "Optimal" if threshold > 127 else "Not Optimal"
            self.threshold_label.config(text=f"Threshold: {threshold:.2f} ({optimal})")

    def show_histogram(self):
        if self.gray_image:
            histogram = compute_histogram(self.gray_image)
            plt.bar(range(256), histogram, color='gray')
            plt.title("Original Histogram")
            plt.xlabel("Pixel Intensity")
            plt.ylabel("Frequency")
            plt.show()

    def equalize_histogram(self):
        if self.gray_image:
            equalized = histogram_equalization(self.gray_image)
            self.equalized_image = equalized
            self.display_image(equalized)
            self.equalized_histogram_btn.config(state=tk.NORMAL)

    def show_equalized_histogram(self):
        if self.equalized_image:
            histogram = compute_histogram(self.equalized_image)
            plt.bar(range(256), histogram, color='gray')
            plt.title("Equalized Histogram")
            plt.xlabel("Pixel Intensity")
            plt.ylabel("Frequency")
            plt.show()

    def analyze_histogram(self):
        if self.gray_image:
            histogram = compute_histogram(self.gray_image)
            total_pixels = sum(histogram)
            uniformity = sum(1 for count in histogram if count > total_pixels * 0.01) / 256
            
            if uniformity > 0.7:
                analysis = "Good: The histogram is fairly uniform, indicating a balanced distribution of pixel intensities."
            else:
                analysis = "Not Good: The histogram is not uniform, it may be poor contrast or unbalanced pixel intensities."
            
            self.analysis_label.config(text=analysis)

    def reset_to_original(self):
        if self.image:
            self.display_image(self.image)
            self.gray_image = None
            self.equalized_image = None
            # Reset button states
            self.histogram_btn.config(state=tk.DISABLED)
            self.equalize_btn.config(state=tk.DISABLED)
            self.equalized_histogram_btn.config(state=tk.DISABLED)
            self.analyze_histogram_btn.config(state=tk.DISABLED)
            self.threshold_label.config(text="Threshold: N/A")
            self.analysis_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = HistogramGUI(root)
    root.mainloop()
