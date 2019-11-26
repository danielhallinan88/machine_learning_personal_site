from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
from config import *
import requests
import time
import os

# View docs: https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
UPLOAD_FOLDER      = 'tmp'
ALLOWED_EXTENSIONS = {'png', 'jpg'}
EXTERNAL_API_IP    = '13.58.166.132'
EXTERNAL_API_PORT  = '8888'
EXTERNAL_API_URL   = 'http://{}:{}'.format(EXTERNAL_API_IP, EXTERNAL_API_PORT)

app = Flask(__name__)
app.config['UPLOAD_FOLDER']    = UPLOAD_FOLDER
app.config['EXTERNAL_API_URL'] = EXTERNAL_API_URL
app.secret_key = b'_5#y2L"Ff943hz\n\xec]/'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/digit-recognizer', methods=["GET", "POST"])
def mnist():
    return render_template("mnist.html")

@app.route('/dog-breed', methods=["GET", "POST"])
def dogBreed():

    if request.method == 'GET':
        return render_template("dogBreed.html")

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            #return redirect(url_for('uploaded_file', filename=filename))

            API_CALL     = 'dog-classifier'
            EXTERNAL_URL = os.path.join(EXTERNAL_API_URL, API_CALL)
            #response     = requests.get(url=EXTERNAL_URL)
            files        = {'image' : open(filepath, 'rb')}

            response     = requests.post(url=EXTERNAL_API_URL, files=files)
            breed = response.text
            print(breed)
            #print(response.request.headers)

            #print(response.status_code)
            #print(response.text)

    return render_template("dogBreed.html")

if __name__ == "__main__":
    app.run(debug=True)
