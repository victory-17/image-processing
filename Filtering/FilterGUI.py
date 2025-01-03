import tkinter as tk
import numpy as np 
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
from Filter import high_pass_filter, low_pass_filter, median_filter_function

class FilterGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Filtering Operations")

        self.canvas = tk.Canvas(master, width=400, height=400, bg='gray')
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        self.controls = tk.Frame(master)
        self.controls.pack(side=tk.RIGHT, padx=10, pady=10)

        # Buttons
        self.upload_btn = tk.Button(self.controls, text="+ Upload Image", bg="green", fg="white", command=self.upload_image)
        self.upload_btn.pack(pady=5)

        self.grayscale_btn = tk.Button(self.controls, text="Convert to Grayscale", bg="darkgray", fg="white", command=self.convert_to_grayscale, state=tk.DISABLED)
        self.grayscale_btn.pack(pady=5)

        self.high_pass_btn = tk.Button(self.controls, text="High-Pass Filter", command=self.apply_high_pass, state=tk.DISABLED)
        self.high_pass_btn.pack(pady=5)

        self.low_pass_btn = tk.Button(self.controls, text="Low-Pass Filter", command=self.apply_low_pass, state=tk.DISABLED)
        self.low_pass_btn.pack(pady=5)

        self.median_btn = tk.Button(self.controls, text="Median Filter", command=self.apply_median_filter, state=tk.DISABLED)
        self.median_btn.pack(pady=5)

        self.reset_btn = tk.Button(self.controls, text="Reset to Original", bg="#000080", fg="white", command=self.reset_image, state=tk.DISABLED)
        self.reset_btn.pack(pady=5)

        self.threshold_btn = tk.Button(self.controls, text="Calculate Threshold", command=self.calculate_threshold, state=tk.DISABLED)
        self.threshold_btn.pack(pady=5)

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
            self.reset_btn.config(state=tk.NORMAL)  # Enable reset button when image is uploaded

    def display_image(self, img):
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.image = img_tk
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

    def convert_to_grayscale(self):
        if self.image:
            gray = ImageOps.grayscale(self.image)
            self.gray_image = gray
            self.display_image(gray)
            self.high_pass_btn.config(state=tk.NORMAL)
            self.low_pass_btn.config(state=tk.NORMAL)
            self.median_btn.config(state=tk.NORMAL)
            self.threshold_btn.config(state=tk.NORMAL)

    def apply_high_pass(self):
        if self.gray_image:
            high_pass_image = high_pass_filter(self.gray_image)
            self.display_image(high_pass_image)

    def apply_low_pass(self):
        if self.gray_image:
            # Choose mask type 1 for demonstration, can be changed to other mask types.
            low_pass_image = low_pass_filter(self.gray_image, mask_type=1)
            self.display_image(low_pass_image)

    def apply_median_filter(self):
        if self.gray_image:
            median_image = median_filter_function(self.gray_image)
            self.display_image(median_image)

    def calculate_threshold(self):
        if self.gray_image:
            np_image = np.array(self.gray_image)
            threshold = np.mean(np_image)
            optimal = "Optimal" if threshold > 127 else "Not Optimal"
            self.threshold_label.config(text=f"Threshold: {threshold:.2f} ({optimal})")

    def reset_image(self):
        if self.image:
            self.display_image(self.image)
            self.gray_image = None
            # Disable filter buttons when reset
            self.high_pass_btn.config(state=tk.DISABLED)
            self.low_pass_btn.config(state=tk.DISABLED)
            self.median_btn.config(state=tk.DISABLED)
            self.threshold_btn.config(state=tk.DISABLED)
            self.threshold_label.config(text="Threshold: N/A")

if __name__ == "__main__":
    root = tk.Tk()
    app = FilterGUI(root)
    root.mainloop()
