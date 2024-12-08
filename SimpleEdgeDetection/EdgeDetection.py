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

    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])

    sobel_y = np.array([[-1, -2, -1],
                        [ 0,  0,  0],
                        [ 1,  2,  1]])
    
    gx = np.array(apply_filter(image, sobel_x), dtype=np.float32)
    gy = np.array(apply_filter(image, sobel_y), dtype=np.float32)
    
    magnitude = np.sqrt(gx**2 + gy**2)
    direction = np.arctan2(gy, gx)
    
    height, width = magnitude.shape
    result = np.zeros((height, width), dtype=np.float32)
    
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            angle = direction[i, j] * 180 / np.pi
            angle = angle % 180
            
            if (0 <= angle < 22.5) or (157.5 <= angle <= 180):
                prev = magnitude[i, j-1]
                next = magnitude[i, j+1]
            elif 22.5 <= angle < 67.5:
                prev = magnitude[i+1, j-1]
                next = magnitude[i-1, j+1]
            elif 67.5 <= angle < 112.5:
                prev = magnitude[i+1, j]
                next = magnitude[i-1, j]
            else:
                prev = magnitude[i-1, j-1]
                next = magnitude[i+1, j+1]
            
            if (magnitude[i, j] >= prev) and (magnitude[i, j] >= next):
                result[i, j] = magnitude[i, j]
    
    result = result * (255.0 / result.max())
    result = np.clip(result, 0, 255)
    return Image.fromarray(result.astype(np.uint8))

def prewitt_operator(image):
    prewitt_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    prewitt_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    
    gx = np.array(apply_filter(image, prewitt_x), dtype=np.float32)
    gy = np.array(apply_filter(image, prewitt_y), dtype=np.float32)
    
    magnitude = np.sqrt(gx**2 + gy**2)
    direction = np.arctan2(gy, gx)
    
    height, width = magnitude.shape
    result = np.zeros((height, width), dtype=np.float32)
    
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            angle = direction[i, j] * 180 / np.pi
            angle = angle % 180
            
            if (0 <= angle < 22.5) or (157.5 <= angle <= 180):
                prev = magnitude[i, j-1]
                next = magnitude[i, j+1]
            elif 22.5 <= angle < 67.5:
                prev = magnitude[i+1, j-1]
                next = magnitude[i-1, j+1]
            elif 67.5 <= angle < 112.5:
                prev = magnitude[i+1, j]
                next = magnitude[i-1, j]
            else:
                prev = magnitude[i-1, j-1]
                next = magnitude[i+1, j+1]
            
            if (magnitude[i, j] >= prev) and (magnitude[i, j] >= next):
                result[i, j] = magnitude[i, j]
    
    result = result * (255.0 / result.max())
    result = np.clip(result, 0, 255)
    return Image.fromarray(result.astype(np.uint8))

def kirsch_operator(image):
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
    
    np_image = np.array(image, dtype=np.float32)
    edges = []
    
    for mask in kirsch_masks:
        edge = apply_filter(image, mask)
        edges.append(np.array(edge, dtype=np.float32))
    
    stacked_edges = np.stack(edges, axis=0)
    max_edges = np.max(stacked_edges, axis=0)
    
    # apply threshold to reduce noise
    threshold = np.mean(max_edges) * 1.5
    max_edges[max_edges < threshold] = 0
    
    if max_edges.max() > 0:  # avoid division by zero
        max_edges = max_edges * (255.0 / max_edges.max())
    
    max_edges = np.clip(max_edges, 0, 255)
    return Image.fromarray(max_edges.astype(np.uint8))
