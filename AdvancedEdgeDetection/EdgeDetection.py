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
    padding = kernel_size // 2  # Calculate padding based on kernel size

    # Pad the image to allow the kernel to cover edges
    padded_image = np.pad(np_image, pad_width=padding, mode='constant', constant_values=0)
    result = np.zeros_like(np_image)

    for i in range(padding, padded_image.shape[0] - padding):
        for j in range(padding, padded_image.shape[1] - padding):
            region = padded_image[i - padding:i + padding + 1, j - padding:j + padding + 1]
            result[i - padding, j - padding] = np.sum(region * kernel)

    result = np.clip(result, 0, 255)  # Ensure the values are within [0, 255]
    return Image.fromarray(result.astype(np.uint8))


def contrast_based_edge(image):
    """
    Apply contrast-based edge detection using the provided edge and smoothing masks.
    Improved method for better edge detection.
    """
    edge_mask = np.array([[-1, 0, -1], [0, 4, 0], [-1, 0, -1]])  # Edge detector mask
    smoothing_mask = np.ones((3, 3)) / 9  # 3x3 smoothing mask

    # Apply edge mask (convolution with edge detector)
    edge_result = apply_filter(image, edge_mask)

    # Apply smoothing mask (convolution for smoothing)
    smoothed_result = apply_filter(image, smoothing_mask)

    # Convert the results to numpy arrays for subtraction
    np_edge_result = np.array(edge_result)
    np_smoothed_result = np.array(smoothed_result)

    # Perform subtraction for edge detection
    contrast_edge = np_edge_result - np_smoothed_result  # More suitable for edge detection

    # Clip the result to [0, 255] and return as image
    contrast_edge = np.clip(contrast_edge, 0, 255)
    return Image.fromarray(contrast_edge.astype(np.uint8))


def difference_of_gaussians(image, kernel_size_1=7, kernel_size_2=9):
    """
    Apply Difference of Gaussians using Gaussian filters with two different kernel sizes.
    This involves blurring with two different kernel sizes and subtracting the results.
    """
    # Apply Gaussian blur with two different kernel sizes
    blurred_1 = gaussian_filter(image, sigma=kernel_size_1 / 6.0)  # Using sigma based on kernel size
    blurred_2 = gaussian_filter(image, sigma=kernel_size_2 / 6.0)  # Using sigma based on kernel size

    # Subtract the blurred images (DoG)
    dog_result = blurred_1 - blurred_2

    # Clip the result to [0, 255] and return as image
    dog_result = np.clip(dog_result, 0, 255)
    return Image.fromarray(dog_result.astype(np.uint8))
