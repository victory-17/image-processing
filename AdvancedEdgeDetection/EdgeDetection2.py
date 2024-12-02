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

def homogeneity_operator(image):
    """
    Apply homogeneity operator to detect edges based on pixel intensity similarity.
    """
    np_image = np.array(image, dtype=np.float32)
    kernel = np.ones((3, 3)) / 9  # A simple averaging kernel to represent similarity
    smoothed_image = apply_filter(image, kernel)

    # Calculate the difference between the central pixel and its neighbors
    homogeneity = np.abs(np_image - smoothed_image)

    homogeneity = np.clip(homogeneity, 0, 255)
    return Image.fromarray(homogeneity.astype(np.uint8))

def difference_operator(image):
    """
    Apply difference operator to detect edges based on intensity differences.
    """
    np_image = np.array(image, dtype=np.float32)
    kernel = np.array([[1, -1, 1], [1, -1, 1], [1, -1, 1]])  # Simple difference operator
    diff_result = apply_filter(image, kernel)

    diff_result = np.clip(diff_result, 0, 255)
    return Image.fromarray(diff_result.astype(np.uint8))

def variance_operator(image):
    """
    Apply variance operator to detect edges based on pixel intensity variance in local neighborhoods.
    """
    np_image = np.array(image, dtype=np.float32)

    # Create a kernel for local neighborhood averaging
    kernel = np.ones((3, 3)) / 9  # A simple averaging kernel for local neighborhood
    smoothed_image = apply_filter(image, kernel)

    # Compute variance for each neighborhood
    variance_result = np.zeros_like(np_image)

    for i in range(1, np_image.shape[0] - 1):
        for j in range(1, np_image.shape[1] - 1):
            # Get a 3x3 region around the current pixel
            region = np_image[i-1:i+2, j-1:j+2]
            # Compute variance of the region
            variance_result[i, j] = np.var(region)

    variance_result = np.clip(variance_result, 0, 255)
    return Image.fromarray(variance_result.astype(np.uint8))

def range_operator(image):
    """
    Apply range operator to detect edges based on intensity range (max - min) in local neighborhoods.
    """
    np_image = np.array(image, dtype=np.float32)
    
    # Create a kernel for local neighborhood averaging
    kernel = np.ones((3, 3)) / 9  # A simple averaging kernel for local neighborhood
    smoothed_image = apply_filter(image, kernel)

    # Compute the range for each neighborhood (max - min)
    range_result = np.zeros_like(np_image)

    for i in range(1, np_image.shape[0] - 1):
        for j in range(1, np_image.shape[1] - 1):
            # Get a 3x3 region around the current pixel
            region = np_image[i-1:i+2, j-1:j+2]
            # Compute the range of the region (max - min)
            range_result[i, j] = np.max(region) - np.min(region)

    range_result = np.clip(range_result, 0, 255)
    return Image.fromarray(range_result.astype(np.uint8))
