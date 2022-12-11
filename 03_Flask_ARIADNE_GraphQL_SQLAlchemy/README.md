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

We also need to install the `mysql` driver by running the following command

```shell
pip install mysqlclient
```

Let's create the `api` folder and inside that api folder we are going to create
a file called `__init__.py` so that api will be a python package. Let's populate
our `__init__.py` with some basic flask simple server code as follows:

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

Let's create a file called `app.py` in the rood dir of our project and add the following
code to it:

```python
# app.py
from api import app
if __name__ == '__main__':
    app.run(debug=True)
```

Now we can go ahead and start the server. We are going to start the server as follows:

```shell
python main.py
```

### Connecting to the database.

Next we are going to connect to the database. We are going to use our local
mysql driver that is already installed on my computer. This is where we are going to
make use of the `SQLAlchemy` package that we have installed. We are going to
navigate to the `api/__init__.py` file and add the following configurations to it.

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

### Creating a model `Post`.

Next we are going to create our simple model Post. We are going to create
another package inside the api called `models`. In this package we will
create our Post model.

```py
# api/models/__init__.py
from api import db

class Post(db.Model):
    # database column
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # the id that we will expose to the user
    postId = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    createdAt = db.Column(db.Date)

    def to_dict(self):
        return {
            "postId": str(self.postId),
            "title": self.title,
            "createdAt": str(self.createdAt)
        }
```

We will go to our application (app.py) file and import the `db` from api and Post from models as follows:

```python
from api import app, db
from api.models import Post

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True, port=3001)
```

We will then run `db.create_all()` when the app started. We only need to run this command
once so that our table get created.

### GraphQL Schema

We are going to create a graphql file called `schema.graphql`. This file will contain
all the schema definitions that we will use in this app. We will add the following code to it:

```graphql
schema {
  query: Query
  mutation: Mutation
}

type Post {
  postId: String!
  title: String!
  createdAt: String!
}

type PostResult {
  success: Boolean!
  errors: [String]
  post: Post
}

type PostsResult {
  success: Boolean!
  errors: [String]
  posts: [Post]
}

type Query {
  getPosts: PostsResult!
  getPost(postId: String!): PostResult
}

type Mutation {
  createPost(title: String!): PostResult!
  updatePost(postId: String!, title: String): PostResult!
  deletePost(postId: String!): Boolean!
}
```

This is how our schema will be looking like. First we defined the schema type which
contains mutation of type Mutation and a query object of type Query. This is the basic graphql
schema that we can create that does the CRUD operations.

Our `Query` type has two resolvers, the one for getting all the posts and the one for
getting a post based on postId.

Our `Mutation` type will have three resolvers that will do the following:

1. create a new post
2. delete a post by id
3. updating a post of a given id

Now inside our `app.py` we are going to add the following code to it:

```python
from api import app, db
from ariadne import QueryType, MutationType, load_schema_from_path, make_executable_schema, graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify

from api.mutation import create_post_resolver, delete_post_resolver, update_post_resolver
from api.queries import get_post_resolver, get_posts_resolver

query = QueryType()
mutation = MutationType()


# Queries
query.set_field("getPosts", get_posts_resolver)
query.set_field("getPost", get_post_resolver)

# Mutations
mutation.set_field("createPost", create_post_resolver)
mutation.set_field("updatePost", update_post_resolver)
mutation.set_field("deletePost", delete_post_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation
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

Next we are going to test our graphql server. You can go to http://127.0.0.1:3001/graphql to use the default playground or you can use the
[GraphQL IDE](http://studio.apollographql.com/dev?utm_source=blog&utm_cta=inline&_gl=1*knbobd*_ga*NTYwMDYwMDI0LjE2MzI5ODY4NTM.*_ga_0BGG5V2W2K*MTYzMzAxMDUzNS4zLjEuMTYzMzAxMTI0OC4w)
. In my case i will use the default playground but if you want the graphql ide go to http://studio.apollographql.com/dev and create an account with email or github. Once you are logged in then set teh endpoint for your graphql server in my case im going to do it as follows:

- Graph title = Posts
- Graph type = Development
- Endpoint http://localhost:3001/graphql

Click `Create Graph` and we are ready to go.

### Creating a Post

We are going to create two packages in the `api` package. The first package will be called
`mutations` and the other one will be called `queries`. In the mutation package
we are going to write our mutations logic and in the queries we are also going to do the same.

As you have seen in the `app.py` we created `mutation` variable of `MutationType` and register our
`createPost` mutation using the `set_field` method to the `create_post_resolver` which looks as follows and can be found in the `mutation` package:

```py
def create_post_resolver(obj, info, title):
    print(obj, info, title)
    try:
        post = Post(
            title=title,
            postId=uuid.uuid4(),
            createdAt=date.today()
        )
        db.session.add(post)
        db.session.commit()
        payload = {
            "success": True,
            "post": post.to_dict()
        }
    except ValueError:
        payload = {
            "success": False,
            "errors": ["something happenned."]
        }
    return payload
```

Now with this resolver we can go to our GraphQL playground and make the following mutation:

```
mutation {
  createPost(title: "this is my awsome posts."){
    success
    errors
    post {
      title
      createdAt
      postId
    }
  }
}
```

And get the following response:

```json
{
  "data": {
    "createPost": {
      "errors": null,
      "post": {
        "createdAt": "2021-10-01",
        "postId": "0dad5bad-733d-404f-a979-9a94ecc02eb0",
        "title": "this is my awsome posts."
      },
      "success": true
    }
  }
}
```

### Updating a post

We need to register our `updatePost` in the `app.py` as follows:

```py
mutation.set_field("updatePost", update_post_resolver)
```

We are registering it to the `update_post_resolver` which looks as follows in the package `mutation`:

```py
def update_post_resolver(obj, info, postId, title):
    try:
        post = Post.query.filter_by(postId=postId).first()
        if post:
            post.title = title
        db.session.add(post)
        db.session.commit()
        payload = {
            "success": True,
            "post": post.to_dict()
        }

    except AttributeError:
        payload = {
            "success": False,
            "errors": ["item matching id {id} not found"]
        }
    return payload
```

If we go to the playground and make the following mutation to update the post:

```
mutation {
  updatePost(postId: "723cc114-cda3-4145-85c2-ec0004cd409c", title: "wow") {
    success
    errors
    post {
      postId
      title
      createdAt
    }
  }
}
```

We get the following response:

```json
{
  "data": {
    "updatePost": {
      "errors": null,
      "post": {
        "createdAt": "2021-10-01",
        "postId": "723cc114-cda3-4145-85c2-ec0004cd409c",
        "title": "wow"
      },
      "success": true
    }
  }
}
```

### Deleting a post

To delete a post the procedure is the same, our `delete_post_resolver` in inside our `mutation` package and it looks as follows:

```py
def delete_post_resolver(obj, info, postId):
    try:
        post = Post.query.filter_by(postId=postId).first()
        db.session.delete(post)
        db.session.commit()
        payload = True
    except AttributeError:
        payload = False
    return payload
```

Now to delete a post we write the following mutation

```
mutation {
  deletePost(postId: "723cc114-cda3-4145-85c2-ec0004cd409c")
}

```

To get the following response:

```json
{
  "data": {
    "deletePost": true
  }
}
```

### Queries

For our queries we have to create a `query` object of type `QueryType` as follows:

```py
query = QueryType()
```

We only have two queries, so next we are going to register them as follows in the `app.py`:

```py
query.set_field("getPosts", get_posts_resolver)
query.set_field("getPost", get_post_resolver)
```

The `get_posts_resolver` and `get_post_resolver` can be found in the `queries` package which have the following code in it:

```py

from api.models import Post
def get_posts_resolver(obj, info):
    try:
        posts = [post.to_dict() for post in Post.query.all()]
        payload = {
            "success": True,
            "posts": posts
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload



def get_post_resolver(obj, info, postId):
    print("getting the posts of id: ", postId)
    try:
        post = Post.query.filter_by(postId=postId).first()
        payload = {
            "success": True,
            "post": post.to_dict()
        }
    except:  # todo not found
        payload = {
            "success": False,
            "errors": ["Post item matching {postId} not found"]
        }
    return payload

```

### Getting as Single post

To get a single post we are going to write the following graphql query in the playground:

```
{
  getPost(postId: "0dad5bad-733d-404f-a979-9a94ecc02eb0") {
    success
    errors
    post {
      title
      postId
      createdAt
    }
  }
}
```

We will get the following response if the postId provided is available in the database:

```json
{
  "data": {
    "getPost": {
      "errors": null,
      "post": {
        "createdAt": "2021-10-01",
        "postId": "0dad5bad-733d-404f-a979-9a94ecc02eb0",
        "title": "this is my awsome posts."
      },
      "success": true
    }
  }
}
```

### Getting all the posts

To get a all the posts we are going to write the following graphql query in the playground:

```
{
  getPosts {
    success
    errors
    posts {
      postId
      title
      createdAt
    }
  }
}

```

In my case i got the following response:

```json
{
  "data": {
    "getPosts": {
      "errors": null,
      "posts": [
        {
          "createdAt": "2021-10-01",
          "postId": "b9242661-659c-4547-a102-85b45f84df63",
          "title": "wow"
        },
        {
          "createdAt": "2021-10-01",
          "postId": "438b41bc-bfed-4409-9c25-03ffc8105ab7",
          "title": "title"
        },
        {
          "createdAt": "2021-10-01",
          "postId": "cac48cf2-1a70-4866-a6bc-de4c232ca733",
          "title": "title"
        },
        {
          "createdAt": "2021-10-01",
          "postId": "1ecf96c6-a508-4909-aa5a-c057df775b2b",
          "title": "title"
        },
        {
          "createdAt": "2021-10-01",
          "postId": "0546994c-026a-492c-ab6a-55a6e33d26b3",
          "title": "title"
        },
        {
          "createdAt": "2021-10-01",
          "postId": "421abc4b-dff4-47a0-a76b-2da3e85b00ff",
          "title": "title"
        },
        {
          "createdAt": "2021-10-01",
          "postId": "3148ba97-bb60-4249-9ab7-047f90279230",
          "title": "title"
        },
        {
          "createdAt": "2021-10-01",
          "postId": "df8fad55-7ca3-45c2-9238-05647168b3be",
          "title": "title"
        },
        {
          "createdAt": "2021-10-01",
          "postId": "2005c7a4-314c-49c2-8c08-e2a8dc9a7ed4",
          "title": "title"
        },
        {
          "createdAt": "2021-10-01",
          "postId": "0dad5bad-733d-404f-a979-9a94ecc02eb0",
          "title": "this is my awsome posts."
        }
      ],
      "success": true
    }
  }
}
```

### Setting up a server for File Uploads

In this section I will show by example how to setup the graphql server in ariadne for doing file uploads.

### Installation

First you need to install the following packages to enable file uploads.

```shell
pip install ariadne[asgi-file-uploads]
```

After that you need to go to your server and change the `graphql_server` endpoint to look as follows:

```py
...
from flask import make_response, jsonify, request, json
from ariadne import  load_schema_from_path, make_executable_schema, graphql_sync, upload_scalar, combine_multipart_data
from ariadne.constants import PLAYGROUND_HTML

type_defs = load_schema_from_path("schema/schema.graphql")
schema = make_executable_schema(
    type_defs, [upload_scalar, query, mutation, ]
)
@app.route("/graphql", methods=["GET"], )
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    if  request.content_type.startswith("multipart/form-data" ):
         data = combine_multipart_data(
            json.loads(request.form.get("operations")),
            json.loads(request.form.get("map")),
            dict(request.files)
        )
    else:
        data =  request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug= AppConfig.DEBUG
    )
    return jsonify(result), 200 if success else 400
```

Now in the schema you can define the `uploadScalar`

```graphql
scalar Upload
```

With only this you will be able to make file uploads to the graphql-server. Here is an example of running a graphql-upload mutation using `cURL`:

```shell

curl http://localhost:3001/graphql -F operations='{ "query": "mutation ClassifyAnimal($input: AnimalInput!) { predictAnimal(input: $input) { error { field message } ok prediction {predictions {  label probability className } } } }", "variables": { "input": {"image": null} } }'  -F map='{ "0": ["variables.input.image"] }'  -F 0=@cat.jpeg
```

That's all about the basic crud operations using `ariadnegraphql` and `python-flask`

### References

1. [blog post](https://www.apollographql.com/blog/graphql/python/complete-api-guide/)
2. [uuid](https://docs.python.org/3/library/uuid.html)
3. [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#configuration-keys)
4. [ariadne](https://ariadnegraphql.org/)
5. [flask-cors](https://flask-cors.readthedocs.io/en/latest/)

6. [ariadnegraphql](https://ariadnegraphql.org/docs/file-uploads#ariadnewsgi)
7. [www.anycodings.com](https://www.anycodings.com/1questions/1507218/upload-file-with-graphql-ariadne-flask-graphqlerrorgraphqlerrorgraphqlerror-operation-data-should-be-a-json-object)
