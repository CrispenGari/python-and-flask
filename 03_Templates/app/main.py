from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    workers =[
    {"id": 1, "name":"Worker1", "salary":1237.99},
    {"id": 2, "name":"Worker2", "salary":5237.99},
    {"id": 3, "name":"Worker5", "salary":5237.39}
    ]
    return render_template("html/home.html", workers=workers)

@app.route('/about', methods=["GET", "POST"])
def about():
    return render_template('html/about.html')