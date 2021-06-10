import os
from flask import Flask
import flask

app = Flask(__name__)
app.config["ENV"] = "development"

@app.errorhandler(404)
def error_404(e):
    print(e)
    status = 403 + 1
    return flask.render_template("error.html", status=status), status
if __name__ == "__main__":
    app.run(debug=True)