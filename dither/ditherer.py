from PIL import Image

color_pallete = [(0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,255,255)]

def adjust_error(color, error):
    return (color[0] + error[0], color[1] + error[1], color[2] + error[2])

def color_dist(c1, c2):
    return (abs(c1[0]-c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2]))

def color_error(c1, c2):
    return c1[0]-c2[0], c1[1] - c2[1], c1[2] - c2[2]

def _get_color(color):
    closest_color = color_pallete[0]
    min_dist = color_dist(color, color_pallete[0])
    error = color_error(color, color_pallete[0])
    for cp in color_pallete:
        new_color_dist = color_dist(color, cp)
        if(new_color_dist < min_dist):
            closest_color = cp
            min_dist = new_color_dist
            error = color_error(color, cp)
    return closest_color, error

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
    forward_array_r = [0.0 for _ in range(width*height)]
    forward_array_g = [0.0 for _ in range(width*height)]
    forward_array_b = [0.0 for _ in range(width*height)]
    for i in range (height):
        for j in range(width):
            new_color, error = _get_color(adjust_error(pixels[i*width+j], (forward_array_r[i*width+j], forward_array_g[i*width+j], forward_array_b[i*width+j])))
            new_pixels.append(new_color)
            distribute_error(forward_array_r, (i,j), error[0], image.size, algorithm)
            distribute_error(forward_array_g, (i,j), error[1], image.size, algorithm)
            distribute_error(forward_array_b, (i,j), error[2], image.size, algorithm)
    image.putdata(new_pixels)
