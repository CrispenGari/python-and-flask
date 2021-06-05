### Sending Files

In this one we want to allow users to get files from the server. Basically we ant users to be able to download files from our page. The same concept applies ob any type of file. In this one we are going to work with images.

### File Structures

Let say we have the following file structuring in our root directory app.

```py
app
    - images
        - img2.png
        uploads
            -img1.png
    - main.py
    ...
```

> `main.py`

```py
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
```

1. `send_from_directory`

- This function is the same as `send_files` it allows us to send a specific file from a directory. The `send_files` allows us to send the contents of a file to the client as well.
- It accepts a lot of parameters which are found [here](https://flask.palletsprojects.com/en/2.0.x/api/#flask.send_from_directory) in the docs.

2. `abort()`

- This function takes http status code and display the message error to the client which matches that status code.

### So what is going on here?

If the user visit http://127.0.0.1:5000/download2/uploads/img1.jpg this will fire the second route with a function `download_2(file_name)`

- The `file_name` is of type path because we want to navigate deeper in our image directory and we want to be able to get the path say `/uploads/img1.jpg` so that we will be able to download it.

If the client visit http://127.0.0.1:5000/download/img2.jpg. This will download the image with the file name `img2/jpg`. The `file_name` in this case is of type string because we don't care about slashes, since our image is in the image directory.

- We passed `as_attachment=True` to allow downloads of the image, otherwise if it is false then the image will be shown in the browser. [Read more about the arguments](https://flask.palletsprojects.com/en/2.0.x/api/#flask.send_from_directory)
