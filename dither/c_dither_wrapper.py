import ctypes

ALGORITHM_DATA = [
([[0, 0, 0, 5, 3],[2, 4, 5, 4, 2],[0, 2, 3, 2, 0]], 2, 32.0),                   #sierra3
([[0, 0, 0, 4, 3],[1, 2, 3, 2, 1]], 2, 16.0),                                   #sierra2
([[0, 0, 2], [1, 1, 0]], 1, 4.0),                                               #sierra1
([[0, 0, 0, 8, 4],[2, 4, 8, 4, 2]], 2, 32.0),                                   #burkes
([[0, 0, 0, 1, 1],[0, 1, 1, 1, 0],[0, 0, 1, 0, 0]],2, 8.0),                     #atkinson
([[0, 0, 0, 8, 4],[2, 4, 8, 4, 2],[1, 2, 4, 2, 1]], 2, 42.0),                   #stucki
([[0, 0, 0, 7, 5],[3, 5, 7, 5, 3],[1, 3, 5, 3, 1]], 2, 48.0),                   #jjn
([[0, 0, 7],[3, 5, 1]], 1, 16.0)                                                #floyd
]

def dither_image(image, algorithm = 0, color_palette = [(0,0,0), (255,255,255)]):
    width, height = image.size
    pixels = image.getdata()
    new_pixels = [0 for _ in range(width*height)]
    cfunc = ctypes.CDLL("./dither/c_dither.so")
    ditherer_pointer = cfunc.get_ditherer(height, width, len(ALGORITHM_DATA[algorithm][0]), ALGORITHM_DATA[algorithm][1]*2+1, int(ALGORITHM_DATA[algorithm][2]))
    print ditherer_pointer
    for i in xrange(len(ALGORITHM_DATA[algorithm][0])):
        for j in xrange(ALGORITHM_DATA[algorithm][1]*2+1):
            cfunc.put_algorithm_data(ALGORITHM_DATA[algorithm][0][i][j], i, j, ditherer_pointer)
    for i in color_palette:
        cfunc.add_color_pallete(i[0], i[1], i[2], ditherer_pointer)
    for i in xrange(height):
        for j in xrange(width):
            raw_color = cfunc.dither_color(pixels[i*width+j][0], pixels[i*width+j][1], pixels[i*width+j][2], ditherer_pointer)
            new_color = (raw_color&255, (raw_color>>8)&255, (raw_color>>16)&255)
            new_pixels[i*width+j] = new_color
    image.putdata(new_pixels)
