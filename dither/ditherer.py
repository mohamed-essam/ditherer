from PIL import Image

BLEEDING_THRESHOLD = 0.9

def adjust_error(color, error):
    return (color[0] + error[0], color[1] + error[1], color[2] + error[2])

def color_dist(c1, c2):
    return (abs(c1[0]-c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2]))

def color_error(c1, c2):
    return c1[0]-c2[0], c1[1] - c2[1], c1[2] - c2[2]

def _get_color(color, color_pallete):
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

def add_error(forward_array, index, error, size, forward_index):
    i, j = index
    w, h = size
    if i < 0 or i >= h or j < 0 or j >= w:
        return
    forward_array[forward_index*w+j] += error

ALGORITHM_DATA = [
([[0, 0, 0, 5, 3],[2, 4, 5, 4, 2],[0, 2, 3, 2, 0]], 2, 32.0)                    #sierra3
([[0, 0, 0, 4, 3],[1, 2, 3, 2, 1]], 2, 16.0)                                    #sierra2
([[0, 0, 2], [1, 1, 0]], 1, 4.0)                                                #sierra1
([[0, 0, 0, 8, 4],[2, 4, 8, 4, 2]], 2, 32.0)                                    #burkes
([[0, 0, 0, 1, 1],[0, 1, 1, 1, 0],[0, 0, 1, 0, 0]],2, 8.0)                      #atkinson
([[0, 0, 0, 8, 4],[2, 4, 8, 4, 2],[1, 2, 4, 2, 1]], 2, 42.0)                    #stucki
([[0, 0, 0, 7, 5],[3, 5, 7, 5, 3],[1, 3, 5, 3, 1]], 2, 48.0)                    #jjn
([[0, 0, 7],[3, 5, 1]], 1, 16.0)                                                #floyd
]

def get_algorithm_data(algorithm):
    return ALGORITHM_DATA[algorithm]


def distribute_error(forward_array, index,error, size, algorithm, forward_index):
    i, j = index
    w, h = size
    error_dist, error_offset, error_divisor = get_algorithm_data(algorithm)
    for k in range(len(error_dist)):
        for l in range(-error_offset, error_offset+1):
            add_error(forward_array, (i+k, j + l), error * error_dist[k][l+error_offset] / error_divisor, size, (forward_index+k)%3)

def dither_image(image, algorithm = 0, color_pallete = [(0,0,0), (255,255,255)]):
    width, height = image.size
    pixels = image.getdata()
    new_pixels = []
    forward_array_r = [0.0 for _ in range(3*width)]
    forward_array_g = [0.0 for _ in range(3*width)]
    forward_array_b = [0.0 for _ in range(3*width)]
    forward_index = 0
    for i in range (height):
        for j in range(width):
            new_color, error = _get_color(adjust_error(pixels[i*width+j], (forward_array_r[forward_index*width+j], forward_array_g[forward_index*width+j], forward_array_b[forward_index*width+j])), color_pallete)
            new_pixels.append(new_color)
            distribute_error(forward_array_r, (i,j), error[0] * BLEEDING_THRESHOLD, image.size, algorithm, forward_index)
            distribute_error(forward_array_g, (i,j), error[1] * BLEEDING_THRESHOLD, image.size, algorithm, forward_index)
            distribute_error(forward_array_b, (i,j), error[2] * BLEEDING_THRESHOLD, image.size, algorithm, forward_index)
        for j in range(width):
            forward_array_r[forward_index*width+j] = forward_array_g[forward_index*width+j] = forward_array_b[forward_index*width+j] = 0.0
        forward_index+=1
        forward_index %= 3
    image.putdata(new_pixels)
