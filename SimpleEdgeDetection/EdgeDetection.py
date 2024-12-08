import numpy as np
import cv2
from PIL import Image, ImageOps

def sobel_operator(image):
    image = np.array(image, dtype=np.float32)
    result_image = np.zeros_like(image, dtype=np.float32)
    height, width = image.shape

    sobel_x_mask = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])

    sobel_y_mask = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ])

    ix = cv2.filter2D(image, -1, sobel_x_mask).astype(np.float32)
    iy = cv2.filter2D(image, -1, sobel_y_mask).astype(np.float32)

    magnitude = np.sqrt(ix ** 2 + iy ** 2).astype(np.float32)
    threshold = np.mean(magnitude)

    for x in range(height):
        for y in range(width):
            if int(magnitude[x, y]) > threshold:
                result_image[x, y] = 255

    return Image.fromarray(result_image.astype(np.uint8))


def prewitt_operator(image):
    image = np.array(image, dtype=np.float32)
    result_image = np.zeros_like(image, dtype=np.float32)
    height, width = image.shape

    prewitt_x_mask = np.array([
        [-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1]
    ])

    prewitt_y_mask = np.array([
        [-1, -1, -1],
        [0, 0, 0],
        [1, 1, 1]
    ])

    ix = cv2.filter2D(image, -1, prewitt_x_mask).astype(np.float32)
    iy = cv2.filter2D(image, -1, prewitt_y_mask).astype(np.float32)

    magnitude = np.sqrt(ix ** 2 + iy ** 2).astype(np.float32)
    threshold = np.mean(magnitude)

    for x in range(height):
        for y in range(width):
            if int(magnitude[x, y]) > threshold:
                result_image[x, y] = 255

    return Image.fromarray(result_image.astype(np.uint8))


def kirsch_compass_masks(image):
    image = np.array(image, dtype=np.float32)
    result_image = np.zeros_like(image, dtype=np.float32)
    height, width = image.shape

    kirsch_masks = [
        np.array([
            [5, 5, 5],
            [-3, 0, -3],
            [-3, -3, -3]
        ]),  # North
        np.array([
            [-3, 5, 5],
            [-3, 0, 5],
            [-3, -3, -3]
        ]),  # Northeast
        np.array([
            [-3, -3, 5],
            [-3, 0, 5],
            [-3, -3, 5]
        ]),  # East
        np.array([
            [-3, -3, -3],
            [-3, 0, 5],
            [-3, 5, 5]
        ]),  # Southeast
        np.array([
            [-3, -3, -3],
            [-3, 0, -3],
            [5, 5, 5]
        ]),  # South
        np.array([
            [-3, -3, -3],
            [5, 0, -3],
            [5, 5, -3]
        ]),  # Southwest
        np.array([
            [5, -3, -3],
            [5, 0, -3],
            [5, -3, -3]
        ]),  # West
        np.array([
            [5, 5, -3],
            [5, 0, -3],
            [-3, -3, -3]
        ])  # Northwest
    ]

    edges = np.array([cv2.filter2D(image, -1, mask) for mask in kirsch_masks])

    magnitude = np.max(edges, axis=0)
    threshold = np.mean(magnitude)

    for x in range(height):
        for y in range(width):
            if int(magnitude[x, y]) > threshold:
                result_image[x, y] = 255

    return Image.fromarray(result_image.astype(np.uint8))
