from PIL import Image

def compute_histogram(image):
    pixels = list(image.getdata())
    histogram = [0] * 256
    for pixel in pixels:
        histogram[pixel] += 1
    return histogram

def histogram_equalization(image):
    width, height = image.size
    total_pixels = width * height
    
    histogram = compute_histogram(image)
    
    # cumulative distribution function
    cdf = [0] * 256
    cdf[0] = histogram[0]
    for i in range(1, 256):
        cdf[i] = cdf[i-1] + histogram[i]
    
    cdf_min = next(x for x in cdf if x > 0)
    
    lut = [0] * 256
    for i in range(256):
        lut[i] = int(round((cdf[i] - cdf_min) / (total_pixels - cdf_min) * 255))
    
    # equalization
    pixels = list(image.getdata())
    equalized_pixels = [lut[p] for p in pixels]
    equalized_image = Image.new('L', (width, height))
    equalized_image.putdata(equalized_pixels)
    return equalized_image
