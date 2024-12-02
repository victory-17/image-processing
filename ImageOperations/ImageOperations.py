import numpy as np
from PIL import Image, ImageOps

def add_images(image):
    np_image = np.array(image, dtype=np.float32)
    np_copy = np.copy(np_image)

    result = np_image + np_copy
    result = np.clip(result, 0, 255)
    return Image.fromarray(result.astype(np.uint8))

def subtract_images(image):
    np_image = np.array(image, dtype=np.float32)
    np_copy = np.copy(np_image)

    result = np_image - np_copy
    result = np.clip(result, 0, 255)
    return Image.fromarray(result.astype(np.uint8))

def invert_image(image):
    np_image = np.array(image, dtype=np.float32)

    inverted_image = 255 - np_image
    inverted_image = np.clip(inverted_image, 0, 255)
    return Image.fromarray(inverted_image.astype(np.uint8))
