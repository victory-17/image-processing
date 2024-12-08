import numpy as np
from PIL import Image


def apply_simple_halftone(image, threshold=128):
    image = np.array(image, dtype=np.float32)
    height, width = image.shape
    result_image = np.zeros_like(image, dtype=np.float32)

    for x in range(height):
        for y in range(width):
            pixel_value = image[x, y]
            if pixel_value > threshold:
                result_image[x, y] = 255

    return Image.fromarray(result_image)


def apply_advanced_halftone(image):
    image = np.array(image, dtype=np.float32)
    height, width = image.shape
    result_image = np.zeros_like(image, dtype=np.float32)

    for x in range(height - 1):
        for y in range(1, width - 1):
            old_pixel = image[x][y]
            new_pixel = 255 if old_pixel > 127 else 0
            result_image[x, y] = new_pixel

            error = old_pixel - new_pixel

            image[x][y + 1] += error * 7 / 16
            image[x + 1][y - 1] += error * 3 / 16
            image[x + 1][y] += error * 5 / 16
            image[x + 1][y + 1] += error * 1 / 16

    return Image.fromarray(result_image.astype(np.uint8))
