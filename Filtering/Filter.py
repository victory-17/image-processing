import numpy as np
from PIL import Image
from scipy.ndimage import median_filter

def apply_filter(image, kernel):
    np_image = np.array(image, dtype=np.float32)
    kernel_size = kernel.shape[0]
    padding = kernel_size // 2  # Calculate padding based on kernel size

    # Pad the image to allow the kernel to cover edges
    padded_image = np.pad(np_image, pad_width=padding, mode='constant', constant_values=0)
    result = np.zeros_like(np_image)

    for i in range(padding, padded_image.shape[0] - padding):
        for j in range(padding, padded_image.shape[1] - padding):
            region = padded_image[i - padding:i + padding + 1, j - padding:j + padding + 1]
            result[i - padding, j - padding] = np.sum(region * kernel)

    result = np.clip(result, 0, 255)
    return Image.fromarray(result.astype(np.uint8))


def high_pass_filter(image):
    high_pass_mask = np.array([[0, -1, 0], 
                               [-1, 5, -1], 
                               [0, -1, 0]])

    return apply_filter(image, high_pass_mask)


def low_pass_filter(image, mask_type=1):
    if mask_type == 1:
        low_pass_mask = np.array([[0, 1, 0], 
                                  [1/6, 2, 1], 
                                  [0, 1, 0]])
    elif mask_type == 2:
        low_pass_mask = np.array([[1, 1, 1], 
                                  [1/9, 1, 1], 
                                  [1, 1, 1]])
    elif mask_type == 3:
        low_pass_mask = np.array([[1, 1, 1], 
                                  [1/10, 2, 1], 
                                  [1, 1, 1]])
    elif mask_type == 4:
        low_pass_mask = np.array([[2, 4, 2], 
                                  [1/16, 2, 1], 
                                  [1, 2, 1]])

    return apply_filter(image, low_pass_mask)


def median_filter_function(image):
    """
    Apply median filter to the image to reduce noise.
    """
    np_image = np.array(image)
    filtered_image = median_filter(np_image, size=3)  # 3x3 median filter
    return Image.fromarray(filtered_image.astype(np.uint8))
