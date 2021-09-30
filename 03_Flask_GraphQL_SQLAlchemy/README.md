### Python Flask and GraphQL

In this one we are going to learn how to create a flask application which
serve as a graphQL API.

### What are we going to use?
We are going to use the following packages:

1. flask
2. ariadne
3. uuid
4. flask-sqlalchemy
5. flask-cors


### Getting started.

1. Create a virtual environment folder
```shell
mkdir venv
```
2. Create a virtual env

```shell
virtualenv ./venv
```
3. Activate the virtual environment

```shell
cd venv && .\Scripts\activate && cd ..
```
### Installation of packages

To install the packages we are going to run the following command.
```shell
pip install flask ariadne uuid flask-cors flask-sqlalchemy
```

We also need to install the ``mysql`` driver by running the following command

```shell
pip install mysqlclient
```

Let's create the ``api`` folder and inside that api folder we are going to create
a file called ``__init__.py`` so that api will be a python package. Let's populate
our ``__init__.py`` with some basic flask simple server code as follows:

```python
# api/__init__.py

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def hello():
    return "hello world", 200

```

Let's create a file called ``app.py`` in the rood dir of our project and add the following
code to it:

````python
# app.py
from api import app
if __name__ == '__main__':
    app.run(debug=True)
````

Now we can go ahead and start the server. We are going to start the server as follows:

````shell
python main.py
````

### Connecting to the database.
Next we are going to connect to the database. We are going to use our local 
mysql driver that is already installed on my computer. This is where we are going to 
make use of the ``SQLAlchemy`` package that we have installed. We are going to
navigate to the ``api/__init__.py`` file and add the following configurations to it.


```python
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/posts"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)

db = SQLAlchemy(app)


@app.route("/", methods=["GET"])
def hello():
    return "hello world", 200

```

### Creating the database `posts`

We are going to create the database that will be able to store our tables. For that open
mysql command line and create a new database by running the following command.

```sql
CREATE DATABASE IF NOT EXISTS posts;
```

### Creating a model ``Post``.
Next we are going to create our simple model Post. We are going to create 
another package inside the api called `models`. In this package we will
create our Post model.

````py
# api/models/__init__.py
from api import db

class Post(db.Model):
    # database column
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # the id that we will expose to the user
    postId = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.Date)

    def to_dict(self):
        return {
            "postId": self.postId,
            "title": self.title,
            "createdAt": str(self.created_at.strftime('%d-%m-%Y'))
        }
````

We will go to our application (app.py) file and import the ``db`` from api and Post from models as follows:

```python
from api import app, db
from api.models import Post

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True, port=3001)
```

We will then run ``db.create_all()`` when the app started. We only need to run this command
once so that our table get created.

### GraphQL Schema

We are going to create a graphql file called ``schema.graphql``. This file will contain
all the schema definitions that we will use in this app. We will add the following code to it:

````graphql
schema {
    query: Query
    mutation: Mutation
}

type Post {
    postId: String!
    title: String!
    created_at: String!
}

type PostResult {
    success: Boolean!
    errors: [String]
    post: Post
}

type PostsResult {
    success: Boolean!
    errors: [String]
    post: [Post]
}

type Query {
    getPosts: PostsResult!
    getPost(postId: String!: PostResult!
}

type Mutation{
     createPost(title: String!, created_at: String): PostResult!
     updatePost(postId: String!, title: String): PostResult!
     deletePost(postId: String!): Boolean!
}
````

This is how our schema will be looking like. First we defined the schema type which
contains mutation of type Mutation and a query object of type Query. This is the basic graphql
schema that we can create that does the CRUD operations. 

Our ``Query`` type has two resolvers, the one for getting all the posts and the one for
getting a post based on postId.

Our `Mutation` type will have three resolvers that will do the following:
1. create a new post
2. delete a post by id
3. updating a post of a given id


Now inside our ``app.py`` we are going to add the following code to it:

```python
from api import app, db
from ariadne import ObjectType, load_schema_from_path, make_executable_schema, graphql_sync, \
    snake_case_fallback_resolvers
from ariadne.constants import PLAYGROUND_HTML
from api.models import Post
from flask import request, jsonify

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, snake_case_fallback_resolvers
)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=True
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True, port=3001)

```

### Testing our GraphQL server
Next we are going to test our graphql server. To do that we need a [GraphQL IDE](http://studio.apollographql.com/dev?utm_source=blog&utm_cta=inline&_gl=1*knbobd*_ga*NTYwMDYwMDI0LjE2MzI5ODY4NTM.*_ga_0BGG5V2W2K*MTYzMzAxMDUzNS4zLjEuMTYzMzAxMTI0OC4w)
. Go to http://studio.apollographql.com/dev and create an account with email or github. Once you are logged in then set teh endpoint for your graphql server in my case im going to do it as follows:

* Graph title = Posts
* Graph type = Development
* Endpoint http://localhost:3001/graphql

Click `Create Graph` and we are ready to go.


### Creating a Post
We are going to create two packages in the `api` package. The first package will be called
``mutations`` and the other one will be called `queries`. In the mutation package
we are going to write our mutations logic and in the queries we are also going to do the same.


1. createPostMutation()








### References
1. [blog post](https://www.apollographql.com/blog/graphql/python/complete-api-guide/)
2. [uuid](https://docs.python.org/3/library/uuid.html)
3. [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#configuration-keys)
4. [ariadne](https://ariadnegraphql.org/)
5. [flask-cors](https://flask-cors.readthedocs.io/en/latest/)