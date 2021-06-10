### Static files

This readme file will be a guide on how we can load static files in flask. First things first, we should have the following folder stuctures:

```python
app-
    - __pycache__
    ...
    - static
        - images
            - image.png
        - js
            - index.js
        - css
            index.css
    - templates
        - index.html
```

> In order to use `flash` we have to import it from `flask`.

- We want to flash some messages when the user has already logged in to the page.
- We want to flash some messages let say when the user is logged out.

> So we are going to modify our files so that they will look as follows:

> `index.js`

```js
document.getElementById("button").addEventListener("click", () => {
  alert("Hello, user!!");
});
```

> `index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link
      rel="stylesheet"
      href="{{url_for('static', filename='css/index.css')}}"
    />
    <title>Form</title>
  </head>
  <body>
    <div class="app">
      <img
        src="{{url_for('static', filename='images/image.jpg')}}"
        alt="nn"
        id="image"
      />
      <button id="button">Hello</button>
    </div>
    <script src="{{url_for('static', filename='js/index.js')}}"></script>
  </body>
</html>
```

> `main.py`

```python
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "abcd"

@app.route('/')
def home_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading
```

> `index.css`

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  color: #333;
}
body {
  background-color: #fafafa;
}
.app {
  width: 100vw;
  height: 100vh;
  overflow-y: hidden;
  overflow-x: hidden;
  display: grid;
  place-items: center;
}
.app > button {
  width: 100px;
  padding: 10px 20px;
  background-color: black;
  color: white;
  cursor: pointer;
  user-select: none;
  user-zoom: none;
  border: none;
  outline: none;
  border-radius: 5px;
}
.app > img {
  border-radius: 5px;
  border-radius: 2px solid green;
}
```

> `image.jpg`

<p align="center">
<img src="https://github.com/CrispenGari/Flask/blob/main/05_Static_Files/app/static/images/image.jpg"/>
</p>

- So now we have a page with some `css`, `js` and an image
