from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/digit-recognizer', methods=["GET", "POST"])
def mnist():
    return render_template("mnist.html")

@app.route('/dog-breed', methods=["GET", "POST"])
def dogBreed():
    return render_template("dogBreed.html")

if __name__ == "__main__":
    app.run(debug=True)
