
from flask import Flask

app = Flask(__name__)
app.config.from_object("config.Production")
@app.route('/')
def home(): 
    return "Home"
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading