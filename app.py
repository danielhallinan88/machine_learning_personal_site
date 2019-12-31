from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
from config import *
import requests
import time
import json
import os

# View docs: https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
UPLOAD_FOLDER      = os.path.join('static', 'images', 'tmp')
ALLOWED_EXTENSIONS = {'png', 'jpg'}
EXTERNAL_API_IP    = '18.216.163.174'
EXTERNAL_API_PORT  = '8888'
EXTERNAL_API_URL   = 'http://{}:{}'.format(EXTERNAL_API_IP, EXTERNAL_API_PORT)

app = Flask(__name__)
app.config['UPLOAD_FOLDER']    = UPLOAD_FOLDER
app.config['EXTERNAL_API_URL'] = EXTERNAL_API_URL
app.secret_key = b'_5#y2L"Ff943hz\n\xec]/'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def answer_dog_query(data):
    dog_breed = data['dog_breed'].replace('_', ' ').capitalize()
    dog = True if data['is_dog'] == 'True' else False
    human = True if data['is_human'] == 'True' else False

    if dog:
        return "That looks like a {}.".format(dog_breed)
    if human:
        return "Hmmm. Seems to be human, but if it was a dog it'd be a {}.".format(dog_breed)

    return "I don't think that counts as a dog or people."

@app.route('/')
@app.route('/index', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/digit-recognizer', methods=["GET", "POST"])
def mnist():
    return render_template("mnist.html")

@app.route('/testcanvas', methods=["GET", "POST"])
def testcanvas():
    return render_template("mnist_canvas.html")
#    return render_template("testcanvas.html")

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

            API_CALL     = 'dog-classifier'
            EXTERNAL_URL = "{}/{}".format(EXTERNAL_API_URL, API_CALL)
            #EXTERNAL_URL = os.path.join(EXTERNAL_API_URL, API_CALL)
            files        = {'image' : open(filepath, 'rb')}
            session      = requests.Session()

            try:
                response     = session.post(EXTERNAL_URL, files=files)

            except requests.exceptions.ConnectionError as e:
                print("Failed to connect to {}".format(EXTERNAL_URL))
                session.close()
                return redirect(request.url)

            session.close()

            #print(response.text)
            dog_string = answer_dog_query(json.loads(response.text))

            #print(response.status_code)
            #print(response.text)
            return render_template("dogBreed.html", image=filepath, dog_string=dog_string)

    return render_template("dogBreed.html")

if __name__ == "__main__":
    app.run(debug=True)
