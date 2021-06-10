### Uploading files to the server

Uploading files to the server is often a requirement of a website or web application. Thankfully, Flask makes this relitively simple for us with a few useful functions.

### An Upload form.

Inside our `index.html` we have a form that looks as follows

```html
<form action="/upload" method="POST" enctype="multipart/form-data">
  <input type="file" name="image" id="image" />
  <button type="submit">Upload</button>
</form>
```

**Make sure the form has the following attribute set**:

```
enctype="multipart/form-data"
```

### Getting the file object in the sever.

To get the file object it is relatively simple we just use the `request.files[""]` instead or `request.form[""]`.

Example:

```py
from flask import Flask, render_template, redirect, request


app = Flask(__name__)
app.config.from_object("config.Development")

@app.route('/upload', methods=["GET", "POST"])
def home():
    if request.files:
        image = request.files["image"]
        print(image) # <FileStorage: '59051957.jfif' ('image/jpeg')>
        redirect(request.url)
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading
```

### Saving files

First you need to create a directory where you will save your images. In our case we are going to create a directory `images`:

```py
app
    -main.py
    -images
    ...
```

This snipped will allow us to upload images from the browser to the `images` folder.

```py

from flask import Flask, render_template, redirect, request
import os

app = Flask(__name__)
app.config.from_object("config.Development")

@app.route('/upload', methods=["GET", "POST"])
def home():
    if request.files:
        image = request.files["image"]
        image.save(os.path.join('./images', image.filename))
        print("Image saved!!")
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading
```

### Securing file uploads

- Ensuring the file has a name
- Ensuring the file type is allowed
- Ensuring the filename is allowed
- Ensuring the file size is allowed

1. Ensuring the file has a name

```py
if request.files["image"] == "":
    return
```

2. Ensuring the file type is allowed

```py
file_types = ["jpg", "jpeg", "png"]

if request.files["image"].split('.')[-1] not in file_types:
    return
```

3. Ensuring the filename is allowed
   Ensuring the filename itself isn't dangerous is probably even more important. Luckily for us, `Werkzeug` provides a handy function called `secure_filename` that we can call to return a secure filename.

```py
from werkzeug.utils import secure_filename
filename = secure_filename(image.filename)
image.save(os.path.join('images', filename))
```

4. Ensuring the file size is allowed

In this case we are going to send a cookie to the browser using javascript with the file size. Then we will get the file size from the browser

```html
<body>
  <form action="/upload" method="POST" enctype="multipart/form-data">
    <input oninput="filesize(this)" type="file" name="image" id="image" />
    <button type="submit">Upload</button>
  </form>
  <script>
    function filesize(elem) {
      document.cookie = `filesize=${elem.files[0].size}`;
    }
  </script>
</body>
```

The following code will ensure that the filesize of the image met the required filesize before posting it to the server

```py
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
```
