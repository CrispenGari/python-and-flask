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