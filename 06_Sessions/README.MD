### Sessions

What is as session variable?

- [Answer](https://stackoverflow.com/questions/3804209/what-are-sessions-how-do-they-work)

In this example we are going to create a login application and keep track of user details using sessions in flask.

To create a web session in flask is actually easy we have to import session from flask. So first thing we should do when creating a session is to specify the secrete key for the app. After the key has been created we can now use sessions to track user's activities on our page.

```python
from flask import session, Flask
app = Flask(__name__)
app.secrete_key = "abc"

# creating a session
session["session_key_name"] = value
```

> `home.html`

```html
<h1>{{user.username}}</h1>
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
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = "abcd"

@app.route('/', methods=["GET", "POST"])
def auth():
    error = ""
    if request.method == "POST":
        if request.form["username"] == 'admin' and  request.form["password"] == '12345':
           session["user"] = {
               "username": request.form["username"],
               "password": request.form["password"]
           }
           return redirect(url_for('home_page'))
        else:
            error="Invalid username or password."
    else:
        error = "Unknown authentication error."
    return render_template('index.html', error=error)

@app.route('/home')
def home_page():
    if session["user"]:
        return render_template('home.html', user=session["user"])
    else:
        return redirect(url_for('auth'))

@app.route('/logout')
def logout():
    session["user"] = None
    return redirect(url_for('auth'))

if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading

```

So we have added the function logout, which essentially, remove the user session when we redirect to the `/logout` route.

### Permanent Session

These sessions keeps the user's activity history until the expiry date. We are going to modify our `main.py` in order for permanent sessions.

> `main.py`

```python
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "abcd"
# setting the lifetime of the session
app.permanent_session_lifetime = timedelta(days=7)

@app.route('/', methods=["GET", "POST"])
def auth():
    error = ""
    if request.method == "POST":
        if request.form["username"] == 'admin' and  request.form["password"] == '12345':
           # Set the session permenant to true
           session.permanent = True
           session["user"] = {
               "username": request.form["username"],
               "password": request.form["password"]
           }
           return redirect(url_for('home_page'))
        else:
            error="Invalid username or password."
    else:
        error = "Unknown authentication error."
    return render_template('index.html', error=error)

@app.route('/home')
def home_page():
    if session["user"]:
        return render_template('home.html', user=session["user"])
    else:
        return redirect(url_for('auth'))

@app.route('/logout')
def logout():
    session["user"] = None
    return redirect(url_for('auth'))

if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading
```
