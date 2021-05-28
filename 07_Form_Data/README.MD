### Handling form data.

In this Readme file we are going to walk through how we can handle form data in `Flask`.

### Example:

Getting the username and password from a form we can do it as follows:

> `index.html`

```html
<body>
  <form action="#" method="post">
    <p><input type="text" name="username" placeholder="username" /></p>
    <p><input type="password" name="password" /></p>
    <button type="submit">Login</button>
  </form>

  <h1>User Details</h1>
  <p><strong>Username: </strong>{{data.username}}</p>
  <p><strong>Password: </strong>{{data.password}}</p>
</body>
```

> `main.py`

```python
from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])
def auth():
    data ={}
    if request.method == "POST":
        data = {
            "username": request.form["username"],
            "password": request.form["password"]
        }
    return render_template('index.html', data=data)
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading
```

Let's create a simple program that will allow the user to login if they have the following credentials.

```
username = "admin"
password = "12345"
```

Then redirect to the home page with their username.

> `home.html`

```html
<h1>{{username}}</h1>
```

> `index.html`

```html
<form action="#" method="post">
  <p><input type="text" name="username" placeholder="username" /></p>
  <p><input type="password" name="password" /></p>
  <p><i>{{error}}</i></p>
  <button type="submit">Login</button>
</form>
```

> `main.py`

```python
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def auth():
    error = ""
    if request.method == "POST":
        if request.form["username"] == 'admin' and  request.form["password"] == '12345':
           return redirect(url_for('home_page', username=request.form["username"]))
        else:
            error="Invalid username or password."
    else:
        error = "Unknown authentication error."
    return render_template('index.html', error=error)

@app.route('/<username>')
def home_page(username):
    print(username)
    return render_template('home.html', username=username)

if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading
```
