from PIL import Image

def _get_luminance(color):
    #RGB
    return (max(color)+min(color))/2.0

def _get_color(lum):
    if lum <= 127.0:
        return ((0,0,0), lum)
    else:
        return  ((255,255,255), lum - 255)

def add_error(forward_array, index, error, size):
    i, j = index
    w, h = size
    if i < 0 or i >= h or j < 0 or j >= w:
        return
    forward_array[i*w+j] += error

def get_algorithm_data(algorithm):
    if algorithm == "sierra3":
        error_dist = [[0, 0, 0, 5, 3],
                      [2, 4, 5, 4, 2],
                      [0, 2, 3, 2, 0]]
        error_offset = 2
        error_divisor = 32.0
    elif algorithm == "sierra2":
        error_dist = [[0, 0, 0, 4, 3],
                      [1, 2, 3, 2, 1]]
        error_offset = 2
        error_divisor = 16.0
    elif algorithm == "sierra1":
        error_dist = [[0, 0, 2],
                      [1, 1, 0]]
        error_offset = 1
        error_divisor = 4.0
    elif algorithm == "burkes":
        error_dist = [[0, 0, 0, 8, 4],
                      [2, 4, 8, 4, 2]]
        error_offset = 2
        error_divisor = 32.0
    elif algorithm == "atkinson":
        error_dist = [[0, 0, 0, 1, 1],
                      [0, 1, 1, 1, 0],
                      [0, 0, 1, 0, 0]]
        error_offset = 2
        error_divisor = 8.0
    elif algorithm == "stucki":
        error_dist = [[0, 0, 0, 8, 4],
                      [2, 4, 8, 4, 2],
                      [1, 2, 4, 2, 1]]
        error_offset = 2
        error_divisor = 42.0
    elif algorithm == "jjn":
        error_dist = [[0, 0, 0, 7, 5],
                      [3, 5, 7, 5, 3],
                      [1, 3, 5, 3, 1]]
        error_offset = 2
        error_divisor = 48.0
    elif algorithm == "floyd":
        error_dist = [[0, 0, 7],
                      [3, 5, 1]]
        error_offset = 1
        error_divisor = 16.0
    return error_dist, error_offset, error_divisor


def distribute_error(forward_array, index,error, size, algorithm):
    i, j = index
    w, h = size
    error_dist, error_offset, error_divisor = get_algorithm_data(algorithm)
    for k in range(len(error_dist)):
        for l in range(-error_offset, error_offset+1):
            add_error(forward_array, (i+k, j + l), error * error_dist[k][l+error_offset] / error_divisor, size)

def dither_image(image, algorithm = "sierra3"):
    width, height = image.size
    pixels = image.getdata()
    new_pixels = []
    forward_array = [0.0 for _ in range(width*height)]
    for i in range (height):
        for j in range(width):
            new_color, error = _get_color(_get_luminance(pixels[i*width+j]) + forward_array[i*width+j])
            new_pixels.append(new_color)
            distribute_error(forward_array, (i,j), error, image.size, algorithm)
    image.putdata(new_pixels)
    return forward_array
