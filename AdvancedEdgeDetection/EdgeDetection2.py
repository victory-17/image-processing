import numpy as np
from PIL import Image

def homogeneity_operator(image, threshold=5):
    image = np.array(image, dtype=np.float32)
    height, width = image.shape
    homogeneity_image = np.zeros_like(image)

    for x in range(1, height - 1):
        for y in range(1, width - 1):
            center_pixel = image[x, y]

            neighborhood = [
                image[x - 1, y - 1], image[x - 1, y], image[x - 1, y + 1],
                image[x, y - 1], image[x, y + 1],
                image[x + 1, y - 1], image[x + 1, y], image[x + 1, y + 1],
            ]

            differences = np.array([abs(center_pixel - neighbor) for neighbor in neighborhood])
            homogeneity_value = max(differences)

            if homogeneity_value > threshold:
                homogeneity_image[x, y] = homogeneity_value

    return Image.fromarray(homogeneity_image.astype(np.uint8))

def difference_operator(image, threshold=5):
    image = np.array(image, dtype=np.float32)
    height, width = image.shape
    difference_image = np.zeros_like(image)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            differences = np.array(
                [
                    abs(image[(i + 1), j] - image[(i - 1), j]),
                    abs(image[i, (j - 1)] - image[i, (j + 1)]),
                    abs(image[(i + 1), (j - 1)] - image[(i - 1), (j + 1)]),
                    abs(image[(i + 1), (j + 1)] - image[(i - 1), (j - 1)]),
                ]
            )

            difference_value = max(differences)

            if difference_value > threshold:
                difference_image[i, j] = difference_value

    return Image.fromarray(difference_image.astype(np.uint8))

def variance_operator(image):
    image = np.array(image, dtype=np.float32)
    height, width = image.shape

    np_image = np.array(image, dtype=np.float32)
    variance_result = np.zeros_like(np_image)

    for x in range(1, height):
        for y in range(1, width):
            neighborhood = image[x - 1: x + 1, y - 1: y + 1]
            mean = np.mean(neighborhood)
            variance = np.sum((neighborhood - mean) ** 2) / 9
            variance_result[x, y] = variance

    return Image.fromarray(variance_result.astype(np.uint8))

def range_operator(image):
    image = np.array(image, dtype=np.float32)
    height, width = image.shape
    range_image = np.zeros_like(image)

    for i in range(1, height):
        for j in range(1, width):
            neighborhood = image[i - 1: i + 1, j - 1: j + 1]
            max_pixel = np.max(neighborhood)
            min_pixel = np.min(neighborhood)
            range_value = max_pixel - min_pixel
            range_image[i, j] = range_value

    return Image.fromarray(range_image.astype(np.uint8))
