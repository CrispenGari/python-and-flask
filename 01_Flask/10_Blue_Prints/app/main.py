from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash
from users.blueprint import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint, url_prefix="/users")

@app.route('/')
def home(): 
    return "Home"
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading