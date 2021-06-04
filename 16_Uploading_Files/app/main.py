import cv2
from flask import Flask, render_template, redirect, request
import os

app = Flask(__name__)
app.config.from_object("config.Development")

allowed_image_filesize = lambda filesize: int(filesize) <= 0.5 * 1024 * 1024

@app.route('/upload', methods=["GET", "POST"])
def home(): 
    print(request.cookies)
    if "filesize" in request.cookies:
        if not allowed_image_filesize(request.cookies.get('filesize')):
            print("File too large")
            return redirect(request.url)
        else:
            print("Uploaded")
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading