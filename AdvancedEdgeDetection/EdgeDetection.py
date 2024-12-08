import cv2
import numpy as np
from PIL import Image, ImageOps

blurring_mask_7x7 = np.array([
    [0, 0, -1, -1, -1, 0, 0],
    [0, -2, -3, -3, -3, -2, 0],
    [-1, -3, 5, 5, 5, -3, -1],
    [-1, -3, 5, 16, 5, -3, -1],
    [-1, -3, 5, 5, 5, -3, -1],
    [0, -2, -3, -3, -3, -2, 0],
    [0, 0, -1, -1, -1, 0, 0],
], dtype=np.float32)

blurring_mask_9x9 = np.array([
    [0, 0, 0, -1, -1, -1, 0, 0, 0],
    [0, -2, -3, -3, -3, -3, -3, -2, 0],
    [0, -3, -2, -1, -1, -1, -2, -3, 0],
    [-1, -3, -1, 9, 9, 9, -1, -3, -1],
    [-1, -3, -1, 9, 19, 9, -1, -3, -1],
    [-1, -3, -1, 9, 9, 9, -1, -3, -1],
    [0, -3, -2, -1, -1, -1, -2, -3, 0],
    [0, -2, -3, -3, -3, -3, -3, -2, 0],
    [0, 0, 0, -1, -1, -1, 0, 0, 0],
], dtype=np.float32)

def contrast_based_edge(image):
    image = np.array(image, dtype=np.float32)

    edge_mask = np.array([
        [-1, 0, -1],
        [ 0, 4,  0],
        [-1, 0, -1]
    ])

    smoothing_mask = np.ones((3, 3)) / 9
    edge_result = cv2.filter2D(image, -1, edge_mask)
    smoothed_result = cv2.filter2D(image, -1, smoothing_mask).astype(np.float32)
    smoothed_result += 1e-10

    contrast_image = edge_result / smoothed_result

    contrast_image = np.clip(contrast_image * 255 / np.max(contrast_image), 0, 255)

    return Image.fromarray(contrast_image.astype(np.uint8))

def difference_of_gaussians(image):
    image = np.array(image)
    blurred_1 = cv2.filter2D(image, -1, blurring_mask_7x7)
    blurred_2 = cv2.filter2D(image, -1, blurring_mask_9x9)

    dog_result = blurred_1 - blurred_2
    return Image.fromarray(dog_result.astype(np.uint8)), Image.fromarray(blurred_1.astype(np.uint8)), Image.fromarray(blurred_2.astype(np.uint8))
