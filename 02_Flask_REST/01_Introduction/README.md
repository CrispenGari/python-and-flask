### Introduction

In this readme we are going to create our first HelloWord REST application. Note that for this we are going to use the `main.py` inside the `../../` root directory for making request. You can use postman to test the routes which we will use later on.

### Our first `get()` route.

> `./main.py`

```py
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
app.config["ENV"] = "development"
api = Api(app)
class HelloWorld(Resource):
    def get(self):
        return {"message":"Hello World"}

api.add_resource(HelloWorld, '/')

if __name__ == "__main__":
    app.run(debug=True)
```

**Note** - The HelloWorld resource is inheriting from the `Resource` and over riding the `get()` http method.

If we go to http://127.0.0.1:5000/ we will get a beautiful 'hello world' message. Now let's try to make a get request at http://127.0.0.1:5000/ using the python `requests` module and see the output looks.

> `../../main.py`

```py
import requests
url = "http://127.0.0.1:5000/"
res = requests.get(url)
print(res.json())

if __name__=="__main__":
    pass
```

**response**:

```json
{ "message": "Hello World" }
```

That's our hello world REST application in flask. Next we are going to create a simple todo application that will post and get data.
