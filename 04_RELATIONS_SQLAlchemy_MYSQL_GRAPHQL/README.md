### Relations SQL Alchemy

In this repository we are going to intergrate relations using `MySQL` and `SQLAlchemy` and GraphQL. We are going to follow [this](https://github.com/CrispenGari/python-flask/tree/main/03_Flask_GraphQL_SQLAlchemy) repository for installation of all the required packages that we will be working with in this README file.

### Connecting to the database.

As i said before we are going to connect to mysql database. So we are going inside the `api/__init__.py` file and add the following code to it:

```py

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/relations"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)

db = SQLAlchemy(app)

```

### Creating the database `relations`

To create the database relations we are going to run the following command in mysql command line client:

```sql
CREATE DATABASE IF NOT EXISTS relations;
```

### One to One Relation.

We are going to create a `one-to-one` relationship between `user` and `profile`. In our models package we are going to have the following code:

```py
from api import db
class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    profileId = db.Column(db.String(50), nullable=False, unique=True)
    gender = db.Column(db.String(15), nullable=False)
    userId = db.Column(db.String(50), db.ForeignKey('user.userId'),
        nullable=False)

    def __repr__(self) -> str:
        return '<Profile %r>' % self.profileId

    def to_dict(self):
         return {
            "userId": str(self.userId),
            "profileId": self.profileId,
            "gender": self.gender
        }

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    userId = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    profile = db.relationship('Profile', backref='profile', lazy=True, uselist=False)

    def __repr__(self) -> str:
        return '<User %r>' % self.username

    def to_dict(self):
         return {
            "userId": str(self.userId),
            "username": self.username,
            "profile": self.profile.to_dict()
        }

```

We are setting `uselist=False` in the `relationship` function so that we tell sqlalchemy that this is a one to one relationship.

### GraphQL Schema

Next we are going to create our graphql schema so that we will be able to persist the user's information in the database using graphql resolvers. We are going to create a `schema.graphql` in the root folder and it will be looking as follows for now:

```ts
schema {
  query: Query
  mutation: Mutation
}

type Profile {
  userId: String!
  profileId: String!
  gender: String!
  user: User
}

type User {
  userId: String!
  username: String!
  profile: Profile
}

type ErrorType {
  field: String!
  message: String!
}

type RegisterUser {
  user: User
  error: ErrorType
}

type ProfileObjectTYpe {
  profile: Profile
  error: ErrorType
}

type Query {
  user(userId: String!): RegisterUser!
  profile(profileId: String!): ProfileObjectTYpe
  hello(username: String): String
}

type Mutation {
  register(username: String!, gender: String!): RegisterUser
}

```

### Register Resolver

We are going to create a subpackage of resolvers called `mutations`. This package will contain all the mutations that we are going to create. We are also going to have `queries` packages which will contain all the queries.

1. Creating a user mutation

```py
# mutations/__init__.py

from api import db
from api.models import Profile, User
from uuid import uuid4
def register_user_resolver(obj, info, username, gender):
    print(username, gender)
    try:
        user = User(
          username=username,
          userId=uuid4()
        )
        db.session.add(user)
        db.session.commit()
        profile = Profile(
            profileId=uuid4(),
            gender=gender,
            userId=user.userId
         )
        db.session.add(profile)
        db.session.commit()
        return {
            "user": user.to_dict(),
            "error": None
        }
    except Exception as e:
      return {
          "user":None,
          "error":{
              "field": "hello",
              "message": str(e)
          }
      }
```

So we first create a and persist in the database. Then we will then create the profile for that user and persist it again in the database. This is done by the use of the `register_user_resolver`

2. Getting a user query

To get a single user with their profile the `user_resolver` will be looking as follows:

```py
# queries/__init__.py
from flask import json
from api import db
from api.models import User, Profile

def user_resolver(obj, info, userId):
    try:
        user = User.query.filter_by(userId=userId).first();
        return {
            "user": user.to_dict(),
            "error": None
        }
    except Exception as e:
        return{
            'user': None,
            "error": str(e)

        }
```

In the `app.py` file we will populate it with the following code:

```py
# app.py
from api import app, db
from ariadne import QueryType, MutationType, load_schema_from_path, make_executable_schema, graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify

from api.resolvers.mutations import register_user_resolver
from api.resolvers.queries import profile_resolver, user_resolver

query = QueryType()
mutation = MutationType()

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation
)

mutation.set_field("register", register_user_resolver)
query.set_field("user", user_resolver)
type_defs = load_schema_from_path("schema.graphql")

schema = make_executable_schema(
    type_defs, mutation, query
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
    db.create_all()
    app.run(debug=True, port=3001)
```

Now with this we are now able to create a users with their profiles using `graphql` playground for example:

For this mutation

```
mutation {
  register(username: "username5", gender: "male") {
    user {
      username
      userId
      profile {
        userId
        gender
        profileId
      }
    }
    error {
      field
      message
    }
  }
}

```

We get the following response

```json
{
  "data": {
    "register": {
      "error": null,
      "user": {
        "profile": {
          "gender": "male",
          "profileId": "75d8c173-767a-4739-a2ef-ee864ed36f01",
          "userId": "e416413c-1e45-4885-9bfd-15f7e98f4a27"
        },
        "userId": "e416413c-1e45-4885-9bfd-15f7e98f4a27",
        "username": "username5"
      }
    }
  }
}
```

Searching the user by `userId`

```
query {
  user(userId: "d25a968e-f9a9-473d-bdb4-85fbbf2ad06f") {
    error {
      field
      message
    }
    user {
      userId
      username
      profile {
        userId
        profileId
        gender
      }
    }
  }
}
```

From teh above query this will be the response that we get.

```json
{
  "data": {
    "user": {
      "error": null,
      "user": {
        "profile": {
          "gender": "male",
          "profileId": "4803a8f7-15f5-4b08-b214-83650786041b",
          "userId": "d25a968e-f9a9-473d-bdb4-85fbbf2ad06f"
        },
        "userId": "d25a968e-f9a9-473d-bdb4-85fbbf2ad06f",
        "username": "username4"
      }
    }
  }
}
```
