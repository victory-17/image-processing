import numpy as np
from PIL import Image

def compute_histogram(image):
    pixels = np.array(image).flatten()
    histogram = [0] * 256
    for pixel in pixels:
        histogram[pixel] += 1
    return histogram

def compute_cdf(histogram):
    cdf = [0] * 256
    cdf[0] = histogram[0]
    for i in range(1, 256):
        cdf[i] = cdf[i-1] + histogram[i]

    return cdf

def histogram_equalization(image):
    image = np.array(image)
    height,  width = image.shape
    
    histogram = compute_histogram(image)
    cdf = compute_cdf(histogram)

    area = width * height
    maximum_gray_level_value = 255
    equalized_image = np.zeros_like(image, dtype=np.uint8)

    # Apply Histogram Equalization
    for x in range(height):
        for y in range(width):
            current_pixel = image[x, y]
            new_pixel_value = int(round(maximum_gray_level_value * cdf[current_pixel] / area))
            equalized_image[x, y] = new_pixel_value

    return Image.fromarray(equalized_image)
