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