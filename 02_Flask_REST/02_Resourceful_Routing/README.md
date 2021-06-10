### Resourceful Routing

The main building block provided by Flask-RESTful are resources. Resources are built on top of Flask pluggable views, giving you easy access to multiple HTTP methods just by defining methods on your resource. In this application we are going to build a certain rest api that will be able to perform the following CRUD operations:

#### A single todo structure

```json
{ "todo1": "Remember the milk" }
```

> `./main.py`

```py
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
```

> `../../main.py`

```py
from requests import put, get
res = put('http://localhost:5000/todo1', data={'data': 'Remember the milk'}).json()
print(res)
input()
print(get('http://localhost:5000/todo1').json())
```

**Output**:

```py
{'todo1': 'Remember the milk'}
{'todo1': 'Remember the milk'}
```

From now on we are going to use postman to make request to the server and create a meaningful application that will allow us to get, post, update and delete from the database.
