from flask import Flask, request, render_template, flash
from werkzeug.utils import secure_filename
from config import *
import requests

# View docs: https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
UPLOAD_FOLDER      = 'tmp'
ALLOWED_EXTENSIONS = {'png'}
EXTERNAL_API_URL   = '18.191.187.159:8888'

app = Flask(__name__)
app.config['UPLOAD_FOLDER']    = UPLOAD_FOLDER
app.config['EXTERNAL_API_URL'] = EXTERNAL_API_URL

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
    #return render_template("dogBreed.html")
    print("YOU WORKING?")
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

            print(EXTERNAL_API_URL)
        #r = requests.post(url=EXTERNAL_API_URL, files=file)
        #print(r.status_code)
        #print(r.text)
    return render_template("dogBreed.html")

if __name__ == "__main__":
    app.run(debug=True)
