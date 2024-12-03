import numpy as np
from PIL import Image, ImageOps

def add_images(image):
    np_image = np.array(image, dtype=np.float32)
    np_copy = np.copy(np_image)
    height, width = np_image.shape[:2]
    
    result = np.zeros_like(np_image)
    for i in range(height):
        for j in range(width):
            if len(np_image.shape) == 3:
                for c in range(3):  # RGB channels
                    result[i,j,c] = min(np_image[i,j,c] + np_copy[i,j,c], 255)
            else:
                result[i,j] = min(np_image[i,j] + np_copy[i,j], 255)
                
    return Image.fromarray(result.astype(np.uint8))

def subtract_images(image):
    np_image = np.array(image, dtype=np.float32)
    np_copy = np.copy(np_image)
    height, width = np_image.shape[:2]
    
    result = np.zeros_like(np_image)
    for i in range(height):
        for j in range(width):
            if len(np_image.shape) == 3:
                for c in range(3):
                    result[i,j,c] = max(np_image[i,j,c] - np_copy[i,j,c], 0)
            else:
                result[i,j] = max(np_image[i,j] - np_copy[i,j], 0)
                
    return Image.fromarray(result.astype(np.uint8))

def invert_image(image):
    np_image = np.array(image, dtype=np.float32)
    height, width = np_image.shape[:2]
    
    result = np.zeros_like(np_image)
    for i in range(height):
        for j in range(width):
            if len(np_image.shape) == 3:
                for c in range(3):
                    result[i,j,c] = 255 - np_image[i,j,c]
            else:
                result[i,j] = 255 - np_image[i,j]
                
    return Image.fromarray(result.astype(np.uint8))
