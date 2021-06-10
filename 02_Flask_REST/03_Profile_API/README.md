## Profile API

In this README we want to create a simple profile api that will allow us to get information about a person. We will use postman to make request to the flask server. We will also use SQLAlchemy as our database.

The user's profile consist of the following:

```py
{
    username: str,
    likes: int,
    id: int,
    comments: int
}
```

First thing first let's create a Profile Resource and add it to our application.

```py
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
app.config["ENV"] = "development"
api = Api(app)


class Profile(Resource):
    def get(self, id):
        return {'id': id}, 200

    def post(self, id):
        return {'id': id}, 201 # status code for created

    def delete(self, id):
        return {'id': id}, 204 # status code for deleted

    def patch(self, id):
        return {'id': id}

api.add_resource(Profile, '/user/<int:id>')

if __name__ == "__main__":
    app.run(debug=True)
```

- We are starting from here. Now let's go ahead and create a database that will store users.

```py
from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["ENV"] = "development"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
api = Api(app)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True, nullable=False)
    username = db.Column("username", db.String(25), nullable=False)
    likes = db.Column("likes", db.Integer, nullable=False)
    comments = db.Column("comments", db.Integer, nullable=False)

    def __init__(self, id, username, likes, comments):
        self.id = id
        self.username = username
        self.likes = likes
        self.comments = comments

    def __repr__(self):
        return f"[username: {self.username}, id: {self.id}, likes: {self.likes}, comments: {self.comments}]"

# db.create_all()
...
```

The rest of the code remains the same. The reason i commented `db.create_all()` is that we don't want our db to be created every time we restart the server. For more on how to create an `SQLAlchemy` model check `01_Flask` series in this repository.

### Profile `post` args.

We have been using `requests.form['key']` from the previous examples to get the data that comes with a query for example the post data. Now we want to use the `flask_restful` `RequestParser()` class that allows us to define what kind of data are we expecting from an http method. Let's code this up and see how it goes.

```py
from flask_restful import Api, Resource, reqparse
...
"""
Args for posting the data
"""
user_post_args = reqparse.RequestParser()
user_post_args.add_argument("username", type=str, help="Username required", required=True)
user_post_args.add_argument("likes", type=int, help="Like required", required=True)
user_post_args.add_argument("comments", type=int, help="Comments required", required=True)
```

- The rest of the code remains the same, we are going to import `reqparse` and then create an instance of `post_args` called `user_post_args` and we are going to add arguments that we will be expecting to come up with our request. We don't need to worry about the id since it will be generated automatically by `sqlite`.

### Data Formatting

Before going futher and do some complicated stuff let's look at data formatting using ` marshal_with()` decorator.By default, all fields in your return iterable will be rendered as-is. While this works great when you’re just dealing with Python data structures, it can become very frustrating when working with objects. To solve this problem, Flask-RESTful provides the fields module and the `marshal_with()` decorator. This decorator accepts the `resource_fields` as it's argument which are typically what we are expecting to be a response. For example in our case we may expect a response like:

```py
{
    id: int,
    username: str,
    likes: int,
    comment: int
}
```

So this will be the structure of our `resource_fields`. Now let's jump into the code.

### What are we getting as user_post_args?

Ok before we jumped into a lot of coding let's visualize the `user_post_args` for the `post` method. Let's change our post function inside the `Profile` resource to look as follows:

```py
class Profile(Resource):
   ...
    def post(self, id):
        args = user_post_args.parse_args()
        return args, 201 # status code for created
    ...
```

Which means if we pass some data along with the post method at a given route for example at http://localhost:5000/user/2 we should get back the data we sent to the server. I'm using postman to post data at the url http://localhost:5000/user/2 and im posting the data as json.

```json
{
  "likes": 10,
  "comments": 16
}
```

If i post the above json we will get the following response:

```json
{
  "message": {
    "username": "Username required"
  }
}
```

This is because during the creation of our `user_post_args` we set the property 'username' to be required

```py
user_post_args.add_argument("username", type=str, help="Username required", required=True)
```

and the help message as "Username required". Which means this message get fired if the username is not provided. The same applies to all the args that we have set. Now let's make another post request with all the data provided and see the response.

```json
{
  "likes": 10,
  "comments": 16,
  "username": "username"
}
```

Response looks as follows:

```json
{
  "username": "username",
  "likes": 10,
  "comments": 16
}
```

**Amazing** Now we want to post this data into the database. Let's go ahead and do that.

We are going to import two things from `flask_restful` which are:

1.  `marshal_with`

- As discussed about data formatting, by default, all fields in your return iterable will be rendered as-is. While this works great when you’re just dealing with Python data structures, it can become very frustrating when working with objects. To solve this problem, Flask-RESTful provides the fields module and the `marshal_with()` decorator.

2. `fields` - allows us to define the fields types that will be returned.

- This decorator accepts the `resource_fields` as it's argument which are typically what we are expecting to be a response. Our resource fields will look as follows:

```python
resource_fields = {
    'id': fields.Integer,
	'username': fields.String,
	'comments': fields.Integer,
	'likes': fields.Integer
}
```

### How do we use this decorator then?

The decorator accepts the `resource_fields` as it arguments and it allows us to return a serialized `user` in our case. The following piece of code shows how we can use it.

```py
@marshal_with(resource_fields)
    def post(self, id):
        args = user_post_args.parse_args()
        user = User(...)
    return user, 201
```

Now if we look at the `post` method in our code is now looking as follows:

```py
@marshal_with(resource_fields)
    def post(self, id):
        args = user_post_args.parse_args()
        """
        Check if the profile exists if not exist create 1 if exist
        return an error using abort()
        """
        result = User.query.filter_by(id=id).first()
        if result:
            abort(409, "User already exists.")
        user = User(id=id, username= args['username'], likes=args['likes'], comments=args['comments'])
        db.session.add(user)
        db.session.commit()
        return user, 201 # status code for created
```

Now if we go to postman and make the following POST request at url http://localhost:5000/user/5:

```json
{
  "likes": 10,
  "comments": 16,
  "username": "username"
}
```

We get the following response:

```json
{
  "id": 5,
  "username": "username",
  "comments": 16,
  "likes": 10
}
```

We are now having a working post method. Let's go ahead and implement the rest of the methods:

**`main.py`**
This is the main.py with the rest of the code.

```py
from flask import Flask, abort
from flask_restful import Api, Resource, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["ENV"] = "development"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
api = Api(app)

"""
Args for posting the data
"""
user_post_args = reqparse.RequestParser()
user_post_args.add_argument("username", type=str, help="Username required", required=True)
user_post_args.add_argument("likes", type=int, help="Like required", required=True)
user_post_args.add_argument("comments", type=int, help="Comments required", required=True)

"""
Args for updating the data (These field must not be required.)
"""
user_patch_args = reqparse.RequestParser()
user_patch_args.add_argument("username", type=str, help="Username required")
user_patch_args.add_argument("likes", type=int, help="Like required")
user_patch_args.add_argument("comments", type=int, help="Comments required")

"""
Resource Fields
"""
resource_fields = {
    'id': fields.Integer,
	'username': fields.String,
	'comments': fields.Integer,
	'likes': fields.Integer
}

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True, nullable=False)
    username = db.Column("username", db.String(25), nullable=False)
    likes = db.Column("likes", db.Integer, nullable=False)
    comments = db.Column("comments", db.Integer, nullable=False)

    def __init__(self, id, username, likes, comments):
        self.id = id
        self.username = username
        self.likes = likes
        self.comments = comments

    def __repr__(self):
        return f"[username: {self.username}, id: {self.id}, likes: {self.likes}, comments: {self.comments}]"

# db.create_all()
profiles = {}
class Profile(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        result = User.query.filter_by(id=id).first()
        if not result:
            abort(404, "User not found.")
        return result, 200

    @marshal_with(resource_fields)
    def post(self, id):
        args = user_post_args.parse_args()
        """
        Check if the profile exists if not exist create 1 if exist
        return an error using abort()
        """
        result = User.query.filter_by(id=id).first()
        if result:
            abort(409, "User already exists.")
        user = User(id=id, username= args['username'], likes=args['likes'], comments=args['comments'])
        db.session.add(user)
        db.session.commit()
        return user, 201 # status code for created

    def delete(self, id):
        result = User.query.filter_by(id=id).first()
        if not result:
            abort(404, "User does not exist.")

        db.session.delete(result)
        db.session.commit()
        return "User deleted", 204 # status code for deleted

    @marshal_with(resource_fields)
    def patch(self, id):
        args = user_patch_args.parse_args()
        result = User.query.filter_by(id=id).first()

        if result:
            if args['username']:
                result.username = args['username']
            if args['likes']:
                result.likes = args['likes']
            if args['comments']:
                result.comments = args['comments']
            db.session.commit()
        else:
            abort(404, "Failed to update, user not found")
        # save updates
        return args, 204
api.add_resource(Profile, '/user/<int:id>')
if __name__ == "__main__":
    app.run(debug=True)
```

- Next -> We are going to create REST API using MongoDB
