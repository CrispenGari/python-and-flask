from flask import Flask, render_template, request
from flask.globals import request
from flask.helpers import make_response

app = Flask(__name__)
app.config["ENV"] = "development"

@app.route('/cookies')
def home():
    res = make_response(render_template("index.html"))
    res.set_cookie("username", "root")
    cookies = request.cookies
    print(cookies)
    return res

if __name__ == "__main__":
    app.run(debug=True)