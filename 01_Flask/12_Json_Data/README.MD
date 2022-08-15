### Json Data.

Json stands for JavaScript Object Notation.

In this README.md file we are going to create a server that will send data from flask app, and be able to post data to a given url.

### Configuring our app

We want to connfigure our application so that it will allow hot reloading on code changes (on save)

Add the following line on top during app creation:

```py
app.config["ENV"] = "development"
```

Then go to the `cmd` and run the following:

```shell
python main.py
```

**Note**: We are going to use **POSTMAN** to make requests and to post data to the server. Let's create our simple server.

We want to say if the the client visit the following url's we want to send the data to the client.

```
http://127.0.0.1:5000/users
    - return all users
http://127.0.0.1:5000/users/id
    - return a user with a given id
```

```python
from flask import Flask, request,  make_response, jsonify


app = Flask(__name__)
app.config["ENV"] = "development"

users = [
    {
        "id": 1,
        "name": "user1",
        "twitter_hander": "@user1",
        "tweet": "This is the tweet from user1."
    },
      {
          "id": 2,
        "name": "user2",
        "twitter_hander": "@user2",
        "tweet": "This is the tweet from user2."
    },
      {
          "id": 3,
        "name": "user3",
        "twitter_hander": "@user3",
        "tweet": "This is the tweet from user3."
    }
]


@app.route('/users', methods=["GET"])
def all_users():
    if request.method == "GET":
        return make_response(jsonify(users), 200)
    else:
        return make_response(jsonify({
            "code": 400,
            "message": "Only Get Methods"
        }))

@app.route('/user/<int:id>', methods=["GET"])
def user(id):
    if request.method == "GET":
        user = None
        for u in users:
            if u["id"] == id:
                user = u
        if user:
            return make_response(jsonify(user), 200)
        else:
            return make_response(jsonify({
                "code": 404,
                "message": f"User with id {id} not found."
            }), 404)
    else:
        return make_response(jsonify({
            "code": 400,
            "message": "Only Get Methods"
        }))

if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading
```

1. **`jsonify()`** - This method converts, python dictionary objects to json files.
2. **`make_response()`** - This method is used to make response by the server to the client.

### Parsing incoming JSON

We want our application to have two way communication, so we want also to be able to send data from the client to the sever. Consider the following code where we are going to post a user to the server.

```py

from flask import Flask, request,  make_response, jsonify


app = Flask(__name__)
app.config["ENV"] = "development"

@app.route('/user', methods=["POST"])
def user():
    if request.method == "POST":
        res = request.get_json()
        print(res)
        return "Done", 200
    else:
        return "Only post method are accepted", 500
if __name__ == "__main__":
    app.run(debug=True) # allow hot reloading
```

Just like the `jsonify` the `get_json()` method grabs a json response from clients and convert it to a python dictionary. The above piece of code will post the data from the client a http://localhost:5000/users. We can protect the sever to accept only json data by adding the following condition.

```py
if request.is_json:
    ....
```

Let's have a look at the following code.

```py

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
```

This will make sure that the data that we are receiving is, json data only.

### More resources

- [HTTP STATUS CODES](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes)
