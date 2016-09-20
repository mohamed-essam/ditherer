from flask import Flask, render_template, request, Response, flash, send_from_directory
from PIL import Image
from dither import c_dither_wrapper
from tempfile import NamedTemporaryFile
from StringIO import StringIO
import json
import urllib2
from base64 import b64encode

application = Flask(__name__, static_url_path='')

@application.route('/<path:path>')
def static_files(path):
    print(path)
    return send_from_directory('static', path)

@application.route('/')
def mainpage():
    return render_template("upload.html")

IMAGE_SIZE_LIMIT = 923601

@application.route('/dither', methods=['POST'])
def dither():
    if request.method == 'POST':
        f = ''
        if 'file' in request.files:
            f = request.files['file']
        elif 'link' in request.form:
            f = urllib2.urlopen(request.form['link'])
        else:
            print "A"
            return 'A', 400
        image = ''
        try:
            image = Image.open(f)
        except:
            print "B"
            return 'B', 400
        color_palette = [(255,255,255), (0,0,0)]
        if 'palette' in request.form:
            try:
                tmp = json.loads(request.form['palette'])
                color_palette = tmp
            except:
                print request.form['palette']
            finally:
                if(len(color_palette) == 0):
                    print "C"
                    return 'C',400
                for i in range(len(color_palette)):
                    if(len(color_palette[i]) != 3):
                        print "D"
                        return "D", 400
                    color_palette[i] = (color_palette[i][0], color_palette[i][1], color_palette[i][2])
        algo = 0
        try:
            if('algorithm' in request.form and int(request.form['algorithm']) in range(8)):
                algo = int(request.form['algorithm'])
        except:
           print request.form['algorithm']
        c_dither_wrapper.dither_image(image, algo, color_palette)
        f.close()
        image_output = StringIO()
        image.save(image_output, "JPEG")
        if 'base64' in request.form and request.form['base64'] == 'True':
            return Response(b64encode(image_output.getvalue()), mimetype="image/jpeg")
        else:
            return Response(image_output.getvalue(), mimetype="image/jpeg")
