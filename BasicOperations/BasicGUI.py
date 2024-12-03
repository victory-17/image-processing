import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import numpy as np

class BasicGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Basic Operations")
        
        self.canvas = tk.Canvas(master, width=400, height=400, bg='gray')
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.controls = tk.Frame(master)
        self.controls.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Buttons
        self.upload_btn = tk.Button(self.controls, text="+ Upload Image", bg="green", fg="white", command=self.upload_image)
        self.upload_btn.pack(pady=5)
        
        self.grayscale_btn = tk.Button(self.controls, text="Convert to Grayscale", command=self.convert_to_grayscale, state=tk.DISABLED)
        self.grayscale_btn.pack(pady=5)
        
        self.threshold_btn = tk.Button(self.controls, text="Calculate Threshold", command=self.calculate_threshold, state=tk.DISABLED)
        self.threshold_btn.pack(pady=5)
        
        self.reset_btn = tk.Button(self.controls, text="Reset to Original", bg="#000080", fg="white", command=self.reset_image, state=tk.DISABLED)
        self.reset_btn.pack(pady=5)
        
        self.threshold_label = tk.Label(self.controls, text="Threshold: N/A", font=("Arial", 12))
        self.threshold_label.pack(pady=5)
        
        self.image = None
        self.gray_image = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((400, 400))  # Resize to fit the canvas
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
            # Convert image to numpy array
            img_array = np.array(self.image)
            
            # Calculate grayscale using weighted sum of RGB channels
            # Using standard weights: R=0.299, G=0.587, B=0.114
            if len(img_array.shape) == 3:  # Check if image is RGB
                gray_array = (0.299 * img_array[:,:,0] + 
                            0.587 * img_array[:,:,1] + 
                            0.114 * img_array[:,:,2]).astype(np.uint8)
                gray = Image.fromarray(gray_array)
            else:  # Image is already grayscale
                gray = self.image
                
            self.gray_image = gray
            self.display_image(gray)

    def calculate_threshold(self):
        if self.gray_image:
            np_image = np.array(self.gray_image)
            
            # Calculate threshold using iterative method (Basic Otsu's method)
            hist = np.histogram(np_image, bins=256, range=(0,256))[0]
            total = np_image.size
            current_max = -float('inf')
            threshold = 0
            
            sum_all = sum(i * h for i, h in enumerate(hist))
            w_b = 0
            sum_b = 0
            
            for i in range(256):
                w_b += hist[i]
                if w_b == 0:
                    continue
                    
                w_f = total - w_b
                if w_f == 0:
                    break
                
                sum_b += i * hist[i]
                mean_b = sum_b / w_b
                mean_f = (sum_all - sum_b) / w_f
                
                # Calculate between class variance
                variance = w_b * w_f * (mean_b - mean_f) ** 2
                
                if variance > current_max:
                    current_max = variance
                    threshold = i
            
            optimal = "Optimal" if threshold > 127 else "Not Optimal"
            self.threshold_label.config(text=f"Threshold: {threshold:.2f} ({optimal})")

    def reset_image(self):
        if self.image:
            self.display_image(self.image)
            self.gray_image = None
            self.threshold_label.config(text="Threshold: N/A")

if __name__ == "__main__":
    root = tk.Tk()
    app = BasicGUI(root)
    root.mainloop()
