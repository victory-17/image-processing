import numpy as np
from PIL import Image

def compute_histogram(image):
    np_image = np.array(image)
    histogram = np.zeros(256, dtype=int)
    for pixel in np_image.ravel():
        histogram[pixel] += 1
    return histogram

def histogram_equalization(image):
    np_image = np.array(image)
    histogram = compute_histogram(image)
    cdf = np.cumsum(histogram)
    cdf_min = np.min(cdf[cdf > 0])  # Exclude zero values
    lut = np.round((cdf - cdf_min) / (np_image.size - cdf_min) * 255).astype(np.uint8)
    equalized_image = lut[np_image]
    return Image.fromarray(equalized_image)
