from ctypes import CDLL, c_int, POINTER, byref
from time import sleep
from multiprocessing import RawArray

ALGORITHM_DATA = [
([[0, 0, 0, 5, 3],[2, 4, 5, 4, 2],[0, 2, 3, 2, 0]], 2, 32),                     #sierra3
([[0, 0, 0, 4, 3],[1, 2, 3, 2, 1]], 2, 16),                                     #sierra2
([[0, 0, 2], [1, 1, 0]], 1, 4),                                                 #sierra1
([[0, 0, 0, 8, 4],[2, 4, 8, 4, 2]], 2, 32),                                     #burkes
([[0, 0, 0, 1, 1],[0, 1, 1, 1, 0],[0, 0, 1, 0, 0]],2, 8),                       #atkinson
([[0, 0, 0, 8, 4],[2, 4, 8, 4, 2],[1, 2, 4, 2, 1]], 2, 42),                     #stucki
([[0, 0, 0, 7, 5],[3, 5, 7, 5, 3],[1, 3, 5, 3, 1]], 2, 48),                     #jjn
([[0, 0, 7],[3, 5, 1]], 1, 16)                                                  #floyd
]

def dither_image(image, algorithm = 0, color_palette = [(0,0,0), (255,255,255)], base = False):
    width, height = image.size
    pixels = image.getdata()
    cfunc = CDLL("./dither/c_dither.so")
    r = RawArray('i', width*height)
    g = RawArray('i', width*height)
    b = RawArray('i', width*height)
    for i in xrange(height):
        for j in xrange(width):
            r[i*width+j] = pixels[i*width+j][0]
            g[i*width+j] = pixels[i*width+j][1]
            b[i*width+j] = pixels[i*width+j][2]
    alg = []
    for i in ALGORITHM_DATA[algorithm][0]:
        for j in i:
            alg.append(j)
    color_pal = []
    for i in color_palette:
        color_pal.append(i[0])
        color_pal.append(i[1])
        color_pal.append(i[2])
    alg_array_type = c_int * len(alg)
    cp_array_type = c_int * len(color_pal)
    cfunc.dither(byref(r), byref(g), byref(b),
     c_int(height), c_int(width),
      byref(alg_array_type(*alg)),
       c_int(len(ALGORITHM_DATA[algorithm][0])),
        c_int(ALGORITHM_DATA[algorithm][1]), c_int(ALGORITHM_DATA[algorithm][2]),
         byref(cp_array_type(*color_pal)), c_int(len(color_palette)))
    for i in xrange(width*height):
        image.putpixel((i%width, i/width), (r[i], g[i], b[i]))
    del r
    del g
    del b
    return image
    image_output = StringIO()
    image.save(image_output, "JPEG")
    if base:
        return Response(b64encode(image_output.getvalue()), mimetype="image/jpeg")
    else:
        return Response(image_output.getvalue(), mimetype="image/jpeg")
