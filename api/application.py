from flask import Flask, render_template, request, Response, flash
from PIL import Image
from dither import ditherer
from tempfile import NamedTemporaryFile
from StringIO import StringIO
import json

application = Flask(__name__)

@application.route('/', methods=['POST'])
def dither():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "", 400
        f = request.files['file']
        image = Image.open(f)
        color_palette = [(255,255,255), (0,0,0)]
        try:
            color_palette = json.loads(request.form['palette'])
        except:
            print request.form['palette']
            pass
        finally:
            if(len(color_palette) == 0):
                return '',400
            for i in range(len(color_palette)):
                if(len(color_palette[i]) != 3):
                    return "", 400
                color_palette[i] = (color_palette[i][0], color_palette[i][1], color_palette[i][2])
        algo = 0
        print(color_palette)
        try:
            if('algorithm' in request.form and int(request.form['algorithm']) in range(8)):
                algo = int(request.form['algorithm'])
        except:
           print request.form['algorithm']
        ditherer.dither_image(image, algo, color_palette)
        f.close()
        image_output = StringIO()
        image.save(image_output, "JPEG")
        return Response(image_output.getvalue(), mimetype="image/png")
