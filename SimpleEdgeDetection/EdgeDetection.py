import numpy as np
from PIL import Image, ImageOps

def apply_filter(image, kernel):
    """
    Applies a convolution filter to the image using the given kernel.
    """
    np_image = np.array(image, dtype=np.float32)
    padded_image = np.pad(np_image, pad_width=1, mode='constant', constant_values=0)
    result = np.zeros_like(np_image)

    for i in range(1, padded_image.shape[0] - 1):
        for j in range(1, padded_image.shape[1] - 1):
            region = padded_image[i - 1:i + 2, j - 1:j + 2]
            result[i - 1, j - 1] = np.sum(region * kernel)

    result = np.clip(result, 0, 255)
    return Image.fromarray(result.astype(np.uint8))

def sobel_operator(image):
    """
    Apply Sobel edge detection.
    """
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    gx = apply_filter(image, sobel_x)
    gy = apply_filter(image, sobel_y)
    magnitude = np.sqrt(np.array(gx)**2 + np.array(gy)**2)
    magnitude = np.clip(magnitude, 0, 255)
    return Image.fromarray(magnitude.astype(np.uint8))

def prewitt_operator(image):
    """
    Apply Prewitt edge detection.
    """
    prewitt_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    prewitt_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    gx = apply_filter(image, prewitt_x)
    gy = apply_filter(image, prewitt_y)
    magnitude = np.sqrt(np.array(gx)**2 + np.array(gy)**2)
    magnitude = np.clip(magnitude, 0, 255)
    return Image.fromarray(magnitude.astype(np.uint8))

def kirsch_operator(image):
    """
    Apply Kirsch compass masks for edge detection.
    """
    kirsch_masks = [
        np.array([[5, 5, 5], [-3, 0, -3], [-3, -3, -3]]),  # North
        np.array([[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]]),  # Northeast
        np.array([[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]]),  # East
        np.array([[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]]),  # Southeast
        np.array([[-3, -3, -3], [-3, 0, -3], [5, 5, 5]]),  # South
        np.array([[-3, -3, -3], [5, 0, -3], [5, 5, -3]]),  # Southwest
        np.array([[5, -3, -3], [5, 0, -3], [5, -3, -3]]),  # West
        np.array([[5, 5, -3], [5, 0, -3], [-3, -3, -3]])   # Northwest
    ]
    max_edges = np.zeros_like(np.array(image), dtype=np.float32)
    for mask in kirsch_masks:
        edge = np.array(apply_filter(image, mask))
        max_edges = np.maximum(max_edges, edge)
    max_edges = np.clip(max_edges, 0, 255)
    return Image.fromarray(max_edges.astype(np.uint8))
