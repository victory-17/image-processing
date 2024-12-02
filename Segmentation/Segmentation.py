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
    hist, bin_edges = np.histogram(np_image, bins=256, range=(0, 255))

    peak = np.argmax(hist)

    segmented_image = np.where(np_image > peak, 255, 0)
    return Image.fromarray(segmented_image.astype(np.uint8))

def histogram_valley_threshold(image):
    """
    Apply histogram valley technique for segmentation.
    Find valleys in the histogram and use them as threshold.
    """
    np_image = np.array(image)
    hist, bin_edges = np.histogram(np_image, bins=256, range=(0, 255))

    valleys, _ = find_peaks(-hist)  # Negative because find_peaks detects maxima, so we negate histogram

    # Choose the first valley as threshold (if available)
    if valleys.size > 0:
        valley_threshold = bin_edges[valleys[0]]
    else:
        valley_threshold = np.min(bin_edges)  # fallback to minimum value if no valley is found

    # Apply the threshold
    segmented_image = np.where(np_image > valley_threshold, 255, 0)
    return Image.fromarray(segmented_image.astype(np.uint8))

def adaptive_histogram_threshold(image):
    """
    Apply adaptive histogram technique for segmentation.
    Uses local mean for adaptive thresholding.
    """
    np_image = np.array(image)
    
    # Apply adaptive thresholding (mean of a 3x3 window)
    adaptive_threshold = filters.threshold_local(np_image, block_size=35, offset=10)
    
    # Apply the adaptive threshold
    segmented_image = np.where(np_image > adaptive_threshold, 255, 0)
    return Image.fromarray(segmented_image.astype(np.uint8))

def calculate_threshold(image):
    """
    Calculate the threshold using the average pixel intensity.
    This could be used for manual segmentation or an additional method.
    """
    np_image = np.array(image)
    threshold = np.mean(np_image)  # Mean intensity as threshold
    return threshold
