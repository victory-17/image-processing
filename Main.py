import tkinter as tk
from tkinter import messagebox
import subprocess

class MainGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Main Menu")
        
        # Set window size
        window_width = 600
        window_height = 900
        self.master.geometry(f"{window_width}x{window_height}")
        
        # Set the default light gray background color
        bg_color = "SystemButtonFace"  # This is the default light gray
        self.master.configure(bg=bg_color)
        
        # Create all widgets with the default light gray background
        self.welcome_label = tk.Label(self.master, 
                                    text="Welcome to Image Processing Tool", 
                                    font=("Inter", 20, "bold"), 
                                    fg="#000080",
                                    bg=bg_color)
        self.welcome_label.pack(pady=20)
        
        self.description_label = tk.Label(self.master, 
                                        text="This program provides various image processing functionalities including edge detection, segmentation, filtering, and more.", 
                                        font=("Inter", 12), 
                                        fg="#000000",
                                        bg=bg_color,
                                        wraplength=550)
        self.description_label.pack(pady=10)
        
        # Button frame
        self.button_frame = tk.Frame(self.master, bg=bg_color)
        self.button_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Buttons without icons
        buttons = [
            ("Basic Operations", self.open_basic_gui),
            ("Simple Edge Detection", self.open_simple_edge_gui),
            ("Segmentation", self.open_segmentation_gui),
            ("Image Operations", self.open_image_operations_gui),
            ("Histogram", self.open_histogram_gui),
            ("Halftoning", self.open_halftoning_gui),
            ("Filtering", self.open_filtering_gui),
            ("Advanced Edge Detection 1", self.open_advanced_edge_gui),
            ("Advanced Edge Detection 2", self.open_advanced_edge2_gui)
        ]
        
        for idx, (text, command) in enumerate(buttons):
            self.create_button(text, command, "#000080", idx)

    def create_button(self, text, command, color, row):
        """Create a button with specified background color and increased spacing"""
        button = tk.Button(self.button_frame, 
                          text=text, 
                          width=30, 
                          height=2, 
                          command=command, 
                          font=("Helvetica", 12, "bold"), 
                          bg=color, 
                          fg="white", 
                          relief="raised", 
                          bd=4,
                          padx=10)  # Add horizontal padding
        button.pack(pady=10, fill="x")  # Increased vertical padding between buttons

    def on_frame_configure(self, event):
        """Update the scrollable region of the canvas whenever the frame is resized"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Open the GUI files
    def open_basic_gui(self):
        subprocess.Popen(["python", "BasicOperations/BasicGUI.py"])

    def open_simple_edge_gui(self):
        subprocess.Popen(["python", "SimpleEdgeDetection/EdgeDetectionGUI.py"])

    def open_segmentation_gui(self):
        subprocess.Popen(["python", "Segmentation/SegmentationGUI.py"])

    def open_image_operations_gui(self):
        subprocess.Popen(["python", "ImageOperations/ImageOperationsGUI.py"])

    def open_histogram_gui(self):
        subprocess.Popen(["python", "Histogram/HistogramGUI.py"])

    def open_halftoning_gui(self):
        subprocess.Popen(["python", "Halftoning/HalftoningGUI.py"])

    def open_filtering_gui(self):
        subprocess.Popen(["python", "Filtering/FilterGUI.py"])

    def open_advanced_edge_gui(self):
        subprocess.Popen(["python", "AdvancedEdgeDetection/EdgeDetectionGUI.py"])

    def open_advanced_edge2_gui(self):
        subprocess.Popen(["python", "AdvancedEdgeDetection/EdgeDetection2GUI.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()
