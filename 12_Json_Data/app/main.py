
from flask import Flask, request,  make_response, jsonify


app = Flask(__name__)
app.config["ENV"] = "development"

@app.route('/user', methods=["POST"])
def user():
    if request.method == "POST":
        if request.is_json:
            res = request.get_json()
            print(res)
            return "Done", 200
        else:
            return "Only json post are allowed", 500
    else:
        return "Only post method are accepted", 500
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading