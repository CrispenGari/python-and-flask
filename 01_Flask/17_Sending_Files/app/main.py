import os
from flask import Flask, request, abort, send_from_directory

app = Flask(__name__)
app.config["ENV"] = "development"

@app.route('/download/<string:file_name>')
def download_1(file_name): 
    try:
        return send_from_directory("./images", path=file_name, as_attachment=True)
    except FileNotFoundError:
            abort(404)
@app.route('/download2/<path:file_name>')
def download_2(file_name): 
    try:
        return send_from_directory("./images", path=file_name, as_attachment=True)
    except FileNotFoundError:
            abort(404)
if __name__ == "__main__":
    app.run(debug=True)