from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home_page():
    data =[
      i for i in range(5)
    ]
    return render_template("home.html", data=data)

"""
@app.route('/')
def home_page():
    return "<h1>Home Page</h1>"

@app.route('/about', methods=["GET", "POST"])
def about_page():
    if request.method == "POST":
        pass # Do something
    else:
        pass # do something
    return "<h1>About Page</h1>"

@app.route('/profile/<username>')
def profile_page(username):
    return f"<h1>About Page {username}</h1>"
"""