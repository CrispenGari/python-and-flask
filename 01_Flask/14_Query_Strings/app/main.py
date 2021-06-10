
from flask import Flask, request
app = Flask(__name__)
app.config["ENV"] = "development"

@app.route('/home')

def home(): 
    if request.query_string:
        print(request.args)
    else:
        print ("No Query String")
    return "Home", 200
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading