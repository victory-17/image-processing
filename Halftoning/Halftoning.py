import numpy as np
from PIL import Image

def simple_halftone(image, threshold=127):
    np_image = np.array(image)
    halftoned = (np_image > threshold) * 255  # Convert to binary (0 or 255)
    return Image.fromarray(halftoned.astype(np.uint8))

def error_diffusion_halftone(image):
    np_image = np.array(image, dtype=np.float32)
    for y in range(np_image.shape[0] - 1):
        for x in range(1, np_image.shape[1] - 1):
            old_pixel = np_image[y, x]
            new_pixel = 255 if old_pixel > 127 else 0
            np_image[y, x] = new_pixel
            error = old_pixel - new_pixel
            np_image[y, x + 1] += error * 7 / 16
            np_image[y + 1, x - 1] += error * 3 / 16
            np_image[y + 1, x] += error * 5 / 16
            np_image[y + 1, x + 1] += error * 1 / 16
    np_image = np.clip(np_image, 0, 255)
    return Image.fromarray(np_image.astype(np.uint8))
