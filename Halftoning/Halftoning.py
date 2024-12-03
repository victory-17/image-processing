import numpy as np
from PIL import Image

def simple_halftone(image, threshold=127):
    width, height = image.size
    result = Image.new('L', (width, height))
    pixels = image.load()
    result_pixels = result.load()
    
    for y in range(height):
        for x in range(width):
            pixel_value = pixels[x, y]
            result_pixels[x, y] = 255 if pixel_value > threshold else 0
            
    return result

def error_diffusion_halftone(image):
    width, height = image.size
    pixels = [[float(image.getpixel((x, y))) for x in range(width)] 
             for y in range(height)]
    result = Image.new('L', (width, height))
    result_pixels = result.load()
    
    for y in range(height - 1):
        for x in range(1, width - 1):
            old_pixel = pixels[y][x]
            new_pixel = 255 if old_pixel > 127 else 0
            result_pixels[x, y] = int(new_pixel)
            
            error = old_pixel - new_pixel
            
            pixels[y][x + 1] += error * 7 / 16
            pixels[y + 1][x - 1] += error * 3 / 16
            pixels[y + 1][x] += error * 5 / 16
            pixels[y + 1][x + 1] += error * 1 / 16
            
            pixels[y][x + 1] = min(255, max(0, pixels[y][x + 1]))
            pixels[y + 1][x - 1] = min(255, max(0, pixels[y + 1][x - 1]))
            pixels[y + 1][x] = min(255, max(0, pixels[y + 1][x]))
            pixels[y + 1][x + 1] = min(255, max(0, pixels[y + 1][x + 1]))
    
    return result
