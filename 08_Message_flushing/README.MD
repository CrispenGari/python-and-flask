### Message flushing.

Message flashing allows us to send messages to our users for example let's say the user has been logged out from our page. We may want to show some messages to them. In this Readme we will just go through the basics of message flashing in flask.

> In order to use `flash` we have to import it from `flask`.

- We want to flash some messages when the user has already logged in to the page.
- We want to flash some messages let say when the user is logged out.

> So we are going to modify our files so that they will look as follows:

> `home.html`

```html
{% with messages = get_flashed_messages() %} {% if messages %} {%for message in
messages%}
<p>{{message}}</p>
{%endfor%} {%endif%} {% endwith %}
<h1>{{user.username}}</h1>
```

> `index.html`

```html
{% with messages = get_flashed_messages() %} {% if messages %} {%for message in
messages%}
<p>{{message}}</p>
{%endfor%} {%endif%} {% endwith %}
<form action="#" method="post">
  <p><input type="text" name="username" placeholder="username" /></p>
  <p><input type="password" name="password" /></p>
  <p><i>{{error}}</i></p>
  <button type="submit">Login</button>
</form>
```

> `main.py`

```python
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "abcd"
app.permanent_session_lifetime = timedelta(days=7)

@app.route('/', methods=["GET", "POST"])
def auth():
    error = ""
    if request.method == "POST":
        if request.form["username"] == 'admin' and  request.form["password"] == '12345':
           session.permanent = True
           session["user"] = {
               "username": request.form["username"],
               "password": request.form["password"]
           }
           flash("Login successful", "info")
           return redirect(url_for('home_page'))
        else:
            error="Invalid username or password."
            flash(error, "info")
    else:
        error = "Unknown authentication error."
    return render_template('index.html', error=error)

@app.route('/home')
def home_page():
    if session["user"]:
        flash("You are logged in.")
        return render_template('home.html', user=session["user"])
    else:
        return redirect(url_for('auth'))

@app.route('/logout')
def logout():
    session["user"] = None
    flash(["You are logged out.", "Login again to access the Home page"], "info")
    return redirect(url_for('auth'))

if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading

```

- If you log in you will receive a message saying you are logged in.
- If you visited `/logout` you will be logged out.

> That's the basics about message flashing.
