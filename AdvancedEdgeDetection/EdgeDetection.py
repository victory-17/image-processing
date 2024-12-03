import numpy as np
from PIL import Image, ImageOps
from scipy.ndimage import gaussian_filter

def apply_filter(image, kernel):
    """
    Applies a convolution filter to the image using the given kernel.
    This function now handles kernels of any size, e.g., 7x7 or 9x9.
    """
    np_image = np.array(image, dtype=np.float32)
    kernel_size = kernel.shape[0]
    padding = kernel_size // 2

    # Pad the image to allow the kernel to cover edges
    padded_image = np.pad(np_image, pad_width=padding, mode='constant', constant_values=0)
    result = np.zeros_like(np_image)

    for i in range(padding, padded_image.shape[0] - padding):
        for j in range(padding, padded_image.shape[1] - padding):
            region = padded_image[i - padding:i + padding + 1, j - padding:j + padding + 1]
            result[i - padding, j - padding] = np.sum(region * kernel)

    result = np.clip(result, 0, 255) 
    return Image.fromarray(result.astype(np.uint8))


def contrast_based_edge(image):
    """
    Apply contrast-based edge detection using the provided edge and smoothing masks
    """
    edge_mask = np.array([[-1, 0, -1],
                          [ 0, 4,  0],
                          [-1, 0, -1]])
    smoothing_mask = np.ones((3, 3)) / 9  # 3x3 smoothing mask

    edge_result = apply_filter(image, edge_mask)

    smoothed_result = apply_filter(image, smoothing_mask)

    np_edge_result = np.array(edge_result)
    np_smoothed_result = np.array(smoothed_result)

    contrast_edge = np_edge_result - np_smoothed_result
    contrast_edge = np.clip(contrast_edge, 0, 255)
    return Image.fromarray(contrast_edge.astype(np.uint8))


def difference_of_gaussians(image, kernel_size_1=7, kernel_size_2=9):
    """
    Apply Difference of Gaussians using Gaussian filters with two different kernel sizes
    => blurring with two different kernel sizes and subtracting the results
    """
    blurred_1 = gaussian_filter(image, sigma=kernel_size_1 / 6.0)
    blurred_2 = gaussian_filter(image, sigma=kernel_size_2 / 6.0) 

    dog_result = blurred_1 - blurred_2
    dog_result = np.clip(dog_result, 0, 255)
    return Image.fromarray(dog_result.astype(np.uint8))
