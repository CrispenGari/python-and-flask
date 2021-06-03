
from flask import Flask, render_template, request
from flask.helpers import make_response
from flask.json import jsonify

app = Flask(__name__)
app.config["ENV"] = "development"

users = [
    {
        "id": 1,
        "username": "user1",
        "message": "This is the message from user1."
    },
      {
          "id": 2,
        "username": "user2",
        "message": "This is the message from user2."
    },
      {
          "id": 3,
        "username": "user3",
        "message": "This is the message from user3."
    }
]
@app.route('/users', methods=["GET"])
def all_users():
    return make_response(jsonify(users), 200)

@app.route('/user', methods=["POST"])
def user():
    if request.method == "POST":
        if request.is_json:
            res = request.get_json()
            # Add to the users database
            print(res)
            return "Created", 201
    return "Error", 500

@app.route('/')
def home(): 
    return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading