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
        color_pallete = [(255,255,255), (0,0,0)]
        try:
            color_pallete = json.loads(request.form['pallete'])
        except:
            pass
        finally:
            if(len(color_pallete) == 0):
                return '',400
            for i in range(len(color_pallete)):
                if(len(color_pallete[i]) != 3):
                    return "", 400
                color_pallete[i] = (color_pallete[i][0], color_pallete[i][1], color_pallete[i][2])
        algo = 0
        print(color_pallete)
        try:
            if('algo' in request.form and int(request.form['algo']) in range (len(ALGORITHMS))):
                algo = int(request.form['algo'])
        except:
            pass
        ditherer.dither_image(image, algo, color_pallete)
        f.close()
        image_output = StringIO()
        image.save(image_output, "PNG")
        return Response(image_output.getvalue(), mimetype="image/png")
