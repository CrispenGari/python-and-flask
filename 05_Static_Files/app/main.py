from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "abcd"

@app.route('/')
def home_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading