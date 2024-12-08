import numpy as np
from PIL import Image
import math

def apply_filter(image, kernel):
    """
    Applies a convolution filter to the image using the given kernel.
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



def create_gaussian_kernel(size, sigma):
    """
    Create a 2D Gaussian kernel
    """
    kernel = np.zeros((size, size))
    center = size // 2
    
    sum_val = 0
    for x in range(size):
        for y in range(size):
            x_dist = x - center
            y_dist = y - center
            # Gaussian function
            kernel[x, y] = math.exp(-(x_dist**2 + y_dist**2)/(2*sigma**2))
            sum_val += kernel[x, y]
    
    return kernel / sum_val

def apply_gaussian_filter(image_array, kernel):
    """
    Apply Gaussian filter using convolution
    """
    if len(image_array.shape) == 3:
        height, width, channels = image_array.shape
    else:
        height, width = image_array.shape
        channels = 1
        image_array = image_array.reshape(height, width, 1)
    
    kernel_size = kernel.shape[0]
    padding = kernel_size // 2
    
    # Create padded image
    padded_image = np.pad(image_array, ((padding, padding), (padding, padding), (0, 0)), mode='reflect')
    result = np.zeros_like(image_array)
    
    # Apply convolution
    for i in range(height):
        for j in range(width):
            for c in range(channels):
                window = padded_image[i:i+kernel_size, j:j+kernel_size, c]
                result[i, j, c] = np.sum(window * kernel)
    
    if channels == 1:
        result = result.reshape(height, width)
    
    return result

def gaussian_filter(image, sigma):
    """
    Main Gaussian filter function
    """
    # Convert PIL Image to numpy array if necessary
    if isinstance(image, Image.Image):
        image_array = np.array(image)
    else:
        image_array = image
    
    # Create kernel size based on sigma
    kernel_size = int(6 * sigma)
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    kernel = create_gaussian_kernel(kernel_size, sigma)
    filtered_image = apply_gaussian_filter(image_array, kernel)
    
    return filtered_image


def difference_of_gaussians(image, kernel_size_1=7, kernel_size_2=9):
    """
    Apply Difference of Gaussians using custom Gaussian filters
    """
    image_array = np.array(image)
    
    blurred_1 = gaussian_filter(image_array, sigma=kernel_size_1 / 6.0)
    blurred_2 = gaussian_filter(image_array, sigma=kernel_size_2 / 6.0)

    dog_result = blurred_1 - blurred_2
    dog_result = np.clip(dog_result, 0, 255)
    
    return Image.fromarray(dog_result.astype(np.uint8))
