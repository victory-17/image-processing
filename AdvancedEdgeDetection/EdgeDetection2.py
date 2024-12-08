import numpy as np
from PIL import Image, ImageOps

def apply_filter(image, kernel):
    np_image = np.array(image, dtype=np.float32)
    kernel_size = kernel.shape[0]
    padding = kernel_size // 2
    padded_image = np.pad(np_image, pad_width=padding, mode='constant', constant_values=0)
    result = np.zeros_like(np_image)

    for i in range(padding, padded_image.shape[0] - padding):
        for j in range(padding, padded_image.shape[1] - padding):
            region = padded_image[i - padding:i + padding + 1, j - padding:j + padding + 1]
            result[i - padding, j - padding] = np.sum(region * kernel)

    result = np.clip(result, 0, 255)
    return Image.fromarray(result.astype(np.uint8))

def homogeneity_operator(image):
    np_image = np.array(image, dtype=np.float32)
    homogeneity = np.zeros_like(np_image)
    
    for i in range(1, np_image.shape[0] - 1):
        for j in range(1, np_image.shape[1] - 1):
            region = np_image[i-1:i+2, j-1:j+2]
            mean = np.sum(region) / 9
            homogeneity[i, j] = abs(np_image[i, j] - mean)

    homogeneity = np.clip(homogeneity, 0, 255)
    return Image.fromarray(homogeneity.astype(np.uint8))

def difference_operator(image):
    np_image = np.array(image, dtype=np.float32)
    kernel = np.array([[1, -1, 1],
                       [1, -1, 1],
                       [1, -1, 1]])
    diff_result = apply_filter(image, kernel)

    diff_result = np.clip(diff_result, 0, 255)
    return Image.fromarray(diff_result.astype(np.uint8))

def variance_operator(image):
    np_image = np.array(image, dtype=np.float32)
    variance_result = np.zeros_like(np_image)

    for i in range(1, np_image.shape[0] - 1):
        for j in range(1, np_image.shape[1] - 1):
            region = np_image[i-1:i+2, j-1:j+2]
            mean = np.sum(region) / 9
            squared_diff_sum = 0
            for x in range(3):
                for y in range(3):
                    squared_diff_sum += (region[x, y] - mean) ** 2
            variance_result[i, j] = squared_diff_sum / 9

    variance_result = np.clip(variance_result, 0, 255)
    return Image.fromarray(variance_result.astype(np.uint8))

def range_operator(image):
    np_image = np.array(image, dtype=np.float32)
    kernel = np.ones((3, 3)) / 9
    smoothed_image = apply_filter(image, kernel)
    range_result = np.zeros_like(np_image)

    for i in range(1, np_image.shape[0] - 1):
        for j in range(1, np_image.shape[1] - 1):
            # 3x3 region around the current pixel
            region = np_image[i-1:i+2, j-1:j+2]
            range_result[i, j] = np.max(region) - np.min(region)

    range_result = np.clip(range_result, 0, 255)
    return Image.fromarray(range_result.astype(np.uint8))
