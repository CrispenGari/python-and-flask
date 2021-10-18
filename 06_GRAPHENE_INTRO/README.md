### Graphene Python

In this one we are going to have a look at how we can make use of graphene to create a simple graphene api in python using python flask.

### Getting started

Run cthe following command to create a virtual environment and activate it:

```shell
mkdir venv && cd venv && virtualenv . && .\Scripts\activate && cd ..
```

### Installation of used packages

We are then going to install the following packages that we will be using.

```shell
pip install SQLAlchemy graphene_sqlalchemy Flask-GraphQL
```

### Creating a schema package.

Next we are going to create a schema package, inside that package we are going to populate with the following code in it:

```py
# schema/__init__.py
from graphene import ObjectType, String, Schema
class Query(ObjectType):
    hello = String(name=String(default_value="world"))
    goodbye = String()
    def resolve_hello(root, info, name):
        return f'Hello {name}!'
    def resolve_goodbye(root, info):
        return 'See ya!'
schema = Schema(query=Query)
```

Next we will create a flask application, so for that go to the root of the folder and create a file called `app.py` and populate it with the following code.

```py
from flask import Flask
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))

if __name__ == '__main__':
    app.run(port=3001, debug=True)

```

Now start the server by running the following command:

```shell
python app.py
```

Go to `http://localhost:3001/graphql` there you will see a `GraphiQL` interface and you will be able to make queries for example:

```
{
  hello
}
```

You will get the following graphql response.

```json
{
  "data": {
    "hello": "Hello world!"
  }
}
```

### References

1. [docs.graphene-python.or](https://docs.graphene-python.org/en/latest/quickstart/)
2. [graphql-python](https://github.com/graphql-python/flask-graphql)
3. [docs.graphene-python.org 2](https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/)
