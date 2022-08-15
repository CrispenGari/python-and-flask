### Class Based View in Flask

In this practical we are going to create a simple REST api on the `Todo` using flask and `SQLAlchemy`. We are going to use the Class Based Views.

### Installation of Packages

```shell
pip install flask Flask-SQLAlchemy
```

First we will create our Todo model in the `models.py` file which will look as follows:

```py

from app import app

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True, nullable=False)
    title = db.Column(db.String(80), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, title, completed):
        self.title = title
        self.completed = completed

    def __repr__(self):
        return '<Student %r>' % self.name

    def to_json(self):
        return {
            'title': self.title,
            'completed': self.completed,
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# creating tables
db.create_all()
```

In our `app` package we are going to have the following code in it:

```py
from datetime import timedelta
from flask import Flask

app = Flask(__name__)

app.secret_key = "abcd"
"""
If SQLALCHEMY_DATABASE_URI is a relative path then we should use 3 slashes
for the uri otherwise 4 slashes.
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=7)
```

In our application we are going to create a `TodoView` class that will inherit from the `MethodView` and write the logic of our http methods. Note that we have the `get`, `post`, `put` and `delete` in our `TodoView` class. When a get http method is fired which means the `get` method in the `TodoView` class will be executed, etc.

Our `app.py` will look as follows:

```py
from datetime import datetime
import imp
from models import db, Todo
from flask.views import MethodView
from app import app
from flask import jsonify, make_response, request


class TodoView(MethodView):
    # http methods
    def get(self, id):
        try:
            if id is None:
                todos = [todo.to_json() for todo in Todo.query.all()]
                return make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 200,
                    'message': "Getting all todos.",
                    'todos': todos
                 })), 200
            else:
                todo =Todo.query.filter_by(id=id).first()
                if todo:
                    return make_response(jsonify({
                        'timestamp': datetime.now(),
                        'code': 200,
                        'message': "Getting a single todo.",
                        'todos': todo.to_json()
                    })), 200
                else:
                    return make_response(jsonify({
                        'timestamp': datetime.now(),
                        'code': 404,
                        'message': f"Todo of id '{id}' was not found.",
                        'todos': None
                    })), 404
        except Exception as e:
            print(e)
            return make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 500,
                    'message': "Internal Server Error."
                 })), 500


    def post(self):
        if request.is_json:
            try:
                data = request.get_json()
                todo = Todo(title=data.get('title'), completed=data.get('completed'))
                db.session.add(todo)
                db.session.commit()
                return make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 201,
                    'message': "Created Todo.",
                    'todo': todo.to_json()
                 })), 201
            except Exception as e:
                return make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 500,
                    'message': "Invalid data."
                 })), 500
        else:
            return make_response(jsonify({
                'timestamp': datetime.now(),
                'code': 500,
                'message': "Only JSON data is allowed."
            })), 500

    def put(self, id):
        try:
            todo =Todo.query.filter_by(id=id).first()
            if todo:
                if request.is_json:
                    try:
                        data = request.get_json()
                        todo.title = data.get('title') if data.get('title') else todo.title
                        todo.completed = data.get('completed') if data.get('completed') else todo.completed
                        db.session.add(todo)
                        db.session.commit()
                        return make_response(jsonify({
                            'timestamp': datetime.now(),
                            'code': 200,
                            'message': "Updated Todo.",
                            'todo': todo.to_json()
                        })), 200
                    except Exception as e:
                        print(e)
                        return make_response(jsonify({
                            'timestamp': datetime.now(),
                            'code': 500,
                            'message': "Invalid data."
                        })), 500
                else:
                    return make_response(jsonify({
                            'timestamp': datetime.now(),
                            'code': 200,
                            'message': "Only json data is allowed.",
                    })), 200
            else:
                return make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 404,
                    'message': f"Todo of id '{id}' was not found.",
                    'todos': None
                })), 404
        except Exception as e:
            print(e)
            return make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 500,
                    'message': "Internal Server Error."
                 })), 500


    def delete(self, id):
        try:
            todo =Todo.query.filter_by(id=id).first()
            if todo:
                db.session.delete(todo)
                db.session.commit()
                return make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 204,
                    'message': f"Deleted todo of id {id}.",
                    'todos': None
                })), 204
            else:
                return make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 404,
                    'message': f"Todo of id '{id}' was not found.",
                    'todos': None
                })), 404
        except Exception as e:
            print(e)
            return make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 500,
                    'message': "Internal Server Error."
                 })), 500


"""
We are going to create a todo_view based on the TodoView because when
we add the url_rule we need a view_func.
"""
todo_view = TodoView.as_view('todo_api')

# Our post method will only have on route
app.add_url_rule('/api/v1/todo', methods=['POST'], view_func=todo_view)

"""
Our get method will have two routes, the one for getting all todos and the other one  for getting
a single todo by id. So we are going to create 2 url rules the one that takes id as None as default
which will be responsible for returning a list of todos
"""
app.add_url_rule('/api/v1/todo', methods=['GET'],
                 defaults={'id' : None}, view_func=todo_view)
app.add_url_rule('/api/v1/todo/<int:id>',
                 methods=['GET', 'PUT', 'DELETE'], view_func=todo_view)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=3001, host='127.0.0.1')
```

Now we can start the server by running the following command:

```shell
python app.py
```

We will be able to send the following requests to the server:

```shell

GET http://127.0.0.1:3001/api/v1/todo/2
GET http://127.0.0.1:3001/api/v1/todo

POST http://127.0.0.1:3001/api/v1/todo

PUT http://127.0.0.1:3001/api/v1/todo/2

DELETE http://127.0.0.1:3001/api/v1/todo/2

# where '2' is the todo id.
```

### Refs

1. [flask.palletsprojects.com](https://flask.palletsprojects.com/en/2.2.x/views/)
