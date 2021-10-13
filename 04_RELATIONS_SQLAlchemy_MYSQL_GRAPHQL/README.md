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
            "profile": self.profile
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
type ProfileResponse {
  profile: Profile
  error: ErrorType
}

type ProfileObjectTYpe {
  profile: Profile
  error: ErrorType
}

type Query {
  user(userId: String!): RegisterUser!
  profile(profileId: String!): ProfileObjectTYpe
}

type Mutation {
  register(username: String!): RegisterUser!
  createProfile(gender: String!, userId: String!): ProfileResponse!
}

```

### Register Resolver

We are going to create a sub-package of resolvers called `mutations`. This package will contain all the mutations that we are going to create. We are also going to have `queries` packages which will contain all the queries.

1. Creating a user and profile mutation

- We are going to allow the user to create their account first and then get an id so that they will then create a profile.

```py
# mutations/__init__.py

def register_user_resolver(obj, info, username):
    print("username", username)
    try:
        user = User(
          username=username,
          userId=uuid4()
        )
        db.session.add(user)
        db.session.commit()
        print(user.to_dict())
        return {
            "user": user,
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

def create_profile_resolver(obj, info, gender, userId):
    try:
        profile = Profile(
            profileId=uuid4(),
            gender=gender,
            userId=userId
         )
        db.session.add(profile)
        db.session.commit()
        return {
            "profile": profile,
            "error": None
        }
    except Exception as e:
      return {
          "profile":None,
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
            "user": user,
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
mutation.set_field("createProfile", create_profile_resolver)

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
  register(username: "username5") {
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
        "profile": null,
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

From the above query this will be the response that we get.

```json
{
  "data": {
    "user": {
      "error": null,
      "user": {
        "profile": null,
        "userId": "d25a968e-f9a9-473d-bdb4-85fbbf2ad06f",
        "username": "username4"
      }
    }
  }
}
```

Now that we have the user let's go and create the profile for the user.

```
mutation {
  createProfile(
    gender: "male"
    userId: "f6118278-fc59-4c79-89d1-063987be3d58"
  ) {
    error {
      field
      message
    }
    profile {
      profileId
      gender
      userId
    }
  }
}
```

Response:

```json
{
  "data": {
    "createProfile": {
      "error": null,
      "profile": {
        "gender": "male",
        "profileId": "8fdf0c9c-3e2c-4b9d-a8fd-5a6974b5a206",
        "userId": "f6118278-fc59-4c79-89d1-063987be3d58"
      }
    }
  }
}
```

Now if we try to get the user with `userId=f6118278-fc59-4c79-89d1-063987be3d58` from the `user-query` here will be the response:

```json
{
  "data": {
    "user": {
      "error": null,
      "user": {
        "profile": {
          "gender": "male",
          "profileId": "48a8dfd4-d2e6-42e0-b6a8-769837da81ef",
          "userId": "f6118278-fc59-4c79-89d1-063987be3d58"
        },
        "userId": "f6118278-fc59-4c79-89d1-063987be3d58",
        "username": "user22"
      }
    }
  }
}
```

### One-to-Many Relationships

We are going to create a one-to-many relationship between a `person` and `address`.

> The most common relationships are one-to-many relationships. Because relationships are declared before they are established you can use strings to refer to classes that are not created yet.

### `Person` and `Address` models

We are going to create the `person` and `address` models in the `models` package and they will be looking as follows:

```py
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    addresses = db.relationship('Address', backref='person', lazy=True)

    # Optional
    def __repr__(self) -> str:
        return '<Person %r>' % self.name

    def to_dict(self):
         return {
            "id": str(self.id),
            "name": self.name,
            "addresses": self.addresses.to_dict()
        }

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)

    # Optional
    def __repr__(self) -> str:
        return '<Address %r>' % self.email

    def to_dict(self):
         return {
            "id": str(self.id),
            "email": self.email,
            "person_id": self.person_id
        }
```

Next we are going to define our graphql types in the `schema.graphql` file. We are going to add to those
existing types, and we are also going to create our mutations and queries in the Mutation and Query type respectively as follows:

```gql
...
input AddressInput {
  email: String!
  person_id: Int!
}

type Address {
  id: Int!
  email: String!
  person_id: Int!
}
type Person {
  id: Int!
  name: String!
  addresses: [Address]!
}
....

type AddressType {
  error: ErrorType
  address: Address
}
type PersonType {
  error: ErrorType
  person: Person
}
type Query {
  ...
  hello(username: String): String
  getPerson(id: Int!): PersonType
}

type Mutation {
  ...
  createAddress(input: AddressInput!): AddressType
  createPerson(name: String!): PersonType
}

```

We have created an `InputType` using the `input` keyword in graphql. This is the same as the `type` but the `type` defines the `ObjectType`. What an `InputType` does is to allow us to create inputs that will be passed directly to our resolvers. We will see this in a moment in action.

We are then going to create add two resolvers in the `mutation` packages which are `create_person_resolver` and `create_email_addresses` as follows:

```py
...
def create_person_resolver(obj, info, name):
    try:
        person = Person(name=name)
        db.session.add(person)
        db.session.commit()
        return {
            "person": person,
            "error": None
        }
    except Exception as e:
      return {
          "person":None,
          "error":{
              "field": "hello",
              "message": str(e)
          }
      }


def create_email_addresses(obj, info, input):
    try:
        try:
            person = Person.query.filter_by(id=input["person_id"]).first()
        except Exception as e:
             return {
                "address":None,
                "error":{
                    "field": "id",
                    "message": str(e)
                }
            }
        address = Address(email=input["email"], person_id=person.id)

        db.session.add(address)
        db.session.commit()
        return {
            "address": address.to_dict(),
            "error": None
        }
    except Exception as e:
      return {
          "address":None,
          "error":{
              "field": "hello",
              "message": str(e)
          }
      }

```

Next we are going to go to the `queries` package and create a `person_query_resolver` which looks as follows:

```py
...
def person_query_resolver(obj, info, id):
    try:
        person = Person.query.filter_by(id=id).first();
        return {
            "person": person,
            "error": None
        }
    except Exception as e:
        return{
            'person': None,
            "error": str(e)

        }
```

Now we are able to persist the person and addresses to the database and get them back. Let's go in the `app.py` file and register our queries and resolvers as follows:

```py
...
mutation.set_field("createAddress", create_email_addresses)
mutation.set_field("createPerson", create_person_resolver)

# Queries
...
query.set_field("getPerson", person_query_resolver)

```

Now restart the server and go to http://127.0.0.1:3001/graphql. In the playground we are going to do the following.

1. Create the Person

```
mutation {
  createPerson(name: "user1") {
    error {
      field
      message
    }
    person {
      id
      name
      addresses {
        id
      }
    }
  }
}
```

Response:

```json
{
  "data": {
    "createPerson": {
      "error": null,
      "person": {
        "addresses": [],
        "id": 3,
        "name": "user1"
      }
    }
  }
}
```

2. Add email addresses to the Person

```
mutation {
  createAddress(input: { email: "test4@gmail.com", person_id: 3 }) {
    error {
      field
      message
    }
    address {
      id
      email
    }
  }
}
```

You can add as more email addresses as you want.

Response:

```json
{
  "data": {
    "createAddress": {
      "address": {
        "email": "test4@gmail.com",
        "id": 3
      },
      "error": null
    }
  }
}
```

To get the user with his or her email addresses we are going to run the following graphql `query`.

```
{
  getPerson(id: 3) {
    error {
      field
      message
    }
    person {
      id
      name
      addresses {
        id
        email
        person_id
      }
    }
  }
}

```

Response

```json
{
  "data": {
    "getPerson": {
      "error": null,
      "person": {
        "addresses": [
          {
            "email": "test@gmail.com",
            "id": 1,
            "person_id": 3
          },
          {
            "email": "test2@gmail.com",
            "id": 2,
            "person_id": 3
          },
          {
            "email": "test4@gmail.com",
            "id": 3,
            "person_id": 3
          }
        ],
        "id": 3,
        "name": "user1"
      }
    }
  }
}
```

> The other code about updating (the address) and deleting (the person) will be found in the code files. Note that we need to add cascades to our database [cascades](https://docs.sqlalchemy.org/en/14/orm/cascades.html)
