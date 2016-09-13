from flask import Flask, render_template, request, Response, flash
from PIL import Image
from dither import ditherer
from tempfile import NamedTemporaryFile
from StringIO import StringIO

application = Flask(__name__)

@application.route('/')
def up():
    return render_template('upload.html')

@application.route('/dither', methods=['GET', 'POST'])
def dither():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        f = request.files['file']
        image = Image.open(f)
        ditherer.dither_image(image, request.form['algo'])
        f.close()
        image_output = StringIO()
        image.save(image_output, "PNG")
        return Response(image_output.getvalue(), mimetype="image/png")
