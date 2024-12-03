import numpy as np
from PIL import Image
from skimage import filters  # for adaptive thresholding
from scipy.signal import find_peaks

def manual_threshold(image, threshold=128):
    """
    Apply manual thresholding technique.
    Threshold values above `threshold` are set to 255, others to 0.
    """
    np_image = np.array(image)
    segmented_image = np.where(np_image > threshold, 255, 0)
    return Image.fromarray(segmented_image.astype(np.uint8))

def histogram_peak_threshold(image):
    """
    Apply histogram peak technique for segmentation.
    The peak of the histogram is found and used as the threshold.
    """
    np_image = np.array(image)
    
    hist = np.zeros(256)
    for pixel in np_image.flatten():
        hist[pixel] += 1
    
    peak = 0
    max_count = 0
    for i in range(256):
        if hist[i] > max_count:
            max_count = hist[i]
            peak = i

    segmented_image = np.where(np_image > peak, 255, 0)
    return Image.fromarray(segmented_image.astype(np.uint8))

def histogram_valley_threshold(image):
    """
    Apply histogram valley technique for segmentation.
    Find valleys in the histogram and use them as threshold.
    """
    np_image = np.array(image)
    
    hist = np.zeros(256)
    for pixel in np_image.flatten():
        hist[pixel] += 1
    
    # Smooth histogram to reduce noise
    window_size = 5
    smoothed_hist = np.zeros(256)
    for i in range(256):
        start = max(0, i - window_size//2)
        end = min(256, i + window_size//2 + 1)
        smoothed_hist[i] = np.mean(hist[start:end])
    
    valleys = []
    for i in range(1, 255):
        if smoothed_hist[i-1] > smoothed_hist[i] < smoothed_hist[i+1]:
            valleys.append(i)
    
    valley_threshold = valleys[0] if valleys else 0

    segmented_image = np.where(np_image > valley_threshold, 255, 0)
    return Image.fromarray(segmented_image.astype(np.uint8))

def adaptive_histogram_threshold(image):
    """
    Apply adaptive histogram technique for segmentation.
    Uses local mean for adaptive thresholding.
    """
    np_image = np.array(image)
    
    # Handle RGB images
    if len(np_image.shape) == 3:
        height, width, channels = np_image.shape
        window_size = 35
        padding = window_size // 2
        
        # Process each channel separately
        segmented_image = np.zeros_like(np_image)
        
        for channel in range(channels):
            channel_data = np_image[:,:,channel]
            padded_channel = np.pad(channel_data, padding, mode='reflect')
            
            for y in range(height):
                for x in range(width):
                    window = padded_channel[y:y+window_size, x:x+window_size]
                    threshold = np.mean(window) - 10
                    # Keep original pixel value if above threshold
                    segmented_image[y, x, channel] = channel_data[y, x] if channel_data[y, x] > threshold else 0
        
    else:  # Grayscale image
        height, width = np_image.shape
        window_size = 35
        padding = window_size // 2
        
        segmented_image = np.zeros_like(np_image)
        padded_image = np.pad(np_image, padding, mode='reflect')
        
        for y in range(height):
            for x in range(width):
                window = padded_image[y:y+window_size, x:x+window_size]
                threshold = np.mean(window) - 10
                segmented_image[y, x] = np_image[y, x] if np_image[y, x] > threshold else 0
    
    return Image.fromarray(segmented_image.astype(np.uint8))

def calculate_threshold(image):
    """
    Calculate the threshold using the average pixel intensity.
    """
    np_image = np.array(image)
    threshold = np.mean(np_image)  # Mean intensity as threshold
    return threshold
