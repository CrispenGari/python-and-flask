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

### Todo example

In this example we are going to create a simple api that does crud operations. We are going to save todos in a list as a local variable and create mutations and queries to fetch and add those todos.

We are first going to create a package called `schema` and add the following code to it.

```py

from graphene import ObjectType,  Schema
import graphene

todos = list()

class Todo(ObjectType):
    title = graphene.String(required=True)
    completed= graphene.Boolean(required=True, default_value=False)
    description = graphene.String(required=False)
    id = graphene.Int(required=True)

class TodoInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    completed= graphene.Boolean(required=True, default_value=False)
    description = graphene.String(required=False)

class TodoResponse(ObjectType):
    error= graphene.String(required=False)
    todo = graphene.Field(Todo)

class CreateTodo(graphene.Mutation):
    class Arguments:
        input_ = TodoInput(required=True)

    ok = graphene.Boolean()
    todo = graphene.Field(lambda: Todo)
    def mutate(root, info, input_=None):
        todo = Todo(
            title = input_.title,
            completed = input_.completed,
            description = input_.description,
            id = len(todos)
        )
        ok = True
        todos.append(todo)
        return CreateTodo(ok=ok, todo=todo)

class UpdateTodo(graphene.Mutation):
    class Arguments:
        input_ = TodoInput(required=True)
        id = graphene.Int(required=True)

    ok = graphene.Boolean()
    todo = graphene.Field(lambda: Todo)

    def mutate(root, info, input_=None, id=None):
        try:
            todo = list(filter(lambda x: x.id == id, todos))[0]
            index = todos.index(todo)
            todo = Todo(
                title = input_.title,
                completed = input_.completed,
                description = input_.description,
                id = id
            )
            todos[index] = todo
            return UpdateTodo(ok=True, todo=todo)
        except:
            return UpdateTodo(ok=False, todo=None)

class DeleteTodo(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()
    def mutate(root, info, id=None):
        global todos
        try:
            todos = list(filter(lambda x: x.id != id, todos))
            return DeleteTodo(ok=True)
        except:
            return DeleteTodo(ok=False)
class Mutation(ObjectType):
    create_todo = CreateTodo.Field(
        name="create_todo",
        description="creating todos"
    )
    delete_todo = DeleteTodo.Field()
    update_todo = UpdateTodo.Field()



class Query(ObjectType):
    todos = graphene.List(graphene.NonNull(Todo))
    todo = graphene.Field(TodoResponse, id=graphene.Int(required=True))

    hello = graphene.String()
    def resolve_todos(root, info):
        return todos

    def resolve_hello(root, info):
        return "hello world"

    def resolve_todo(root, info, id):
        try:
            todo = list(filter(lambda x: x.id == id, todos))[0]
            return TodoResponse(
            error = None,
            todo=todo
           )
        except:
            return TodoResponse(
                error = f"todo of id {id} was not found.",
                todo=None
            )
schema = Schema(query=Query, mutation=Mutation)
```

With the above code we will be able to make the following mutations and queries at http://localhost:3001/graphql

### Mutations

1. creating a todo

```
mutation {
  create_todo(
    input_: {
      title: "cleaning"
      completed: false
      description: "cleaning the house."
    }
  ) {
    ok
    todo {
      title
      completed
      id
      description
    }
  }
}


```

response:

```json
{
  "data": {
    "create_todo": {
      "ok": true,
      "todo": {
        "title": "cleaning",
        "completed": false,
        "id": 0,
        "description": "cleaning the house."
      }
    }
  }
}
```

2. updating a todo

```
mutation {
  updateTodo(
    id: 1
    input_: {
      title: "cleaning...."
      completed: false
      description: "cleaning the house."
    }
  ) {
    ok
    todo {
      title
      completed
      id
      description
    }
  }
}

```

response:

```json
{
  "data": {
    "updateTodo": {
      "ok": false,
      "todo": null
    }
  }
}
```

3. deleting a todo

```
mutation{
  deleteTodo(id: 0){
    ok
  }
}
```

response:

```json
{
  "data": {
    "deleteTodo": {
      "ok": true
    }
  }
}
```

### Queries

1. hello world

```

{
  hello
}
```

response:

```json
{
  "data": {
    "hello": "hello world"
  }
}
```

2. getting all todos

```
{
  todos {
    title
    completed
    id
    description
  }
}

```

response:

```json
{
  "data": {
    "todos": [
      {
        "title": "cleaning",
        "completed": false,
        "id": 0,
        "description": "cleaning the house."
      }
    ]
  }
}
```

3. getting a single todo

```
{
  todo(id: 0) {
    error
    todo{
      completed
      title
      description
      id
    }
  }
}


```

response:

```json
{
  "data": {
    "todo": {
      "error": null,
      "todo": {
        "completed": false,
        "title": "cleaning",
        "description": "cleaning the house.",
        "id": 0
      }
    }
  }
}
```

In the `app.py` we are going to have the following code:

```python

from flask_graphql import GraphQLView
from schema import schema
# from api import app, db

app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))

if __name__ == '__main__':
    # db.create_all()
    app.run(port=3001, debug=True)
```

### What are we going to build?

We are going to create a simple GraphQL api which consist of users and notes. Where notes and users are sqlalchamey models.

```shell
pip install python-dotenv flask-jwt-extended bcrypt graphene_sqlalchemy
```

### SqlAlchemy and Graphene

The next task is to be able to create users and save them into the database using `sqlalchemy` and graphene. For that we are going to create a model `User` in the `models` package and it will look as follows:

```py
from api import db
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    userId = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    def __repr__(self) -> str:
        return '<User %r>' % self.username
```

### Getting all the users

Next we will go to the `schema` package and add the following code to it:

```py
class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )

class Query(ObjectType):
    node = relay.Node.Field() # required
    users = SQLAlchemyConnectionField(User)
    ...
schema = Schema(query=Query, mutation=Mutation)
```

With these modifications we can be able to write the following query to the graphql api:

```
{
  users {
    edges {
      node {
        id
        username
        userId
      }
    }
  }
}
```

We will get the following response from the api.

```json
{
  "data": {
    "users": {
      "edges": []
    }
  }
}
```

### Adding users to the database.

To add a user we are going to modify the code in the `schema` package and add a mutation and input type as follows:

```py

class AddUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    user = graphene.Field(lambda: User)
    ok = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, input):
        user = UserModel(uuid4(), input["username"])
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return AddUser(user=None, ok=False, error=e)
        return AddUser(user=user, ok=True, error=None)

class Mutation(ObjectType):
    ....
    add_user = AddUser.Field()
...
schema = Schema(query=Query, mutation=Mutation)
```

Now we will be able to make the following mutation on the graphql.

```
mutation {
  addUser(input: { username: "username" }) {
    ok
    user {
      id
      userId
      username
    }
  }
}
```

We will get the following response from the api.

```json
{
  "data": {
    "addUser": {
      "ok": true,
      "user": {
        "id": "VXNlcjox",
        "userId": "40cb7ca6-0d48-443d-bb63-e8a4e6947410",
        "username": "username"
      }
    }
  }
}
```

### Deleting the user

To delete the user we are going to modify our package `schema` to have the mutation `DeleteUser` which looks as follows:

We can now be able to run the following mutation in the playground.

```
mutation {
  deleteUser(id: "40cb7ca6-0d48-443d-bb63-e8a4e6947410") {
    ok
    error
  }
}

```

We get the following response if the user with the given id does not exists, otherwise the user will be deleted from the database.

```json
{
  "data": {
    "deleteUser": {
      "ok": false,
      "error": "the username with that id does not exists."
    }
  }
}
```

### References

1. [docs.graphene-python.or](https://docs.graphene-python.org/en/latest/quickstart/)
2. [graphql-python](https://github.com/graphql-python/flask-graphql)
3. [docs.graphene-python.org 2](https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/)
