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

### Updating a person address.

To update the person address we are going to add the following under the Mutation Type in the `schema.graphql` file:

```
...
type Mutation {
  ...
  updateAddress(input: UpdateAddressInput!): AddressType!
  deletePerson(id: Int!): Boolean! # this is for deleting the person
}
```

Now we will head over to our mutations an create the `update_email_addresses` resolver which will look as follows:

```py
def update_email_addresses(obj, info, input):
    try:
        try:
            address = Address.query.filter_by(id=input["id"]).first()

        except Exception as e:
             return {
                "address":None,
                "error":{
                    "field": "id",
                    "message": str(e)
                }
            }

        # check the validity of the email
        address.email = input["email"]
        db.session.commit()
        return {
            "address": address,
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

Next we are going to register our new resolver in the `app.py` as follows:

```py
...
mutation.set_field("deletePerson", delete_person_resolver) # this is for deleting the person
mutation.set_field("updateAddress", update_email_addresses)
...
```

Now we will be able to make the following graphql mutation of updating the email address of the person.

```
mutation {
  updateAddress(input: { email: "email.gmail.com", id: 4 }) {
    address {
      id
      email
      person_id
    }
    error {
      field
      message
    }
  }
}

```

We will get the following response:

```json
{
  "data": {
    "updateAddress": {
      "address": {
        "email": "email.gmail.com",
        "id": 4,
        "person_id": 3
      },
      "error": null
    }
  }
}
```

### Deleting the person

Note that when deleting the person, we also need to delete the addresses of that person. You can change this behavior by setting the cascades which you can read in the [docs](https://docs.sqlalchemy.org/en/14/orm/cascades.html).

In our case we want to delete the child related objects to the person, so we are going to set the cascade in the person entity as follows:

```
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    addresses = db.relationship('Address', backref='person', lazy=True, cascade="all, delete")
   ...
```

We set the `cascade="all, delete"` on the `db.relationship` on the addresses. The `backref="person"` allows us to reference the person in the address by calling `address.person`

Now we will add the `delete_person_resolver` in the `mutations` package as follows

```py
def delete_person_resolver(obj, info, id):
    try:
        person = Person.query.filter_by(id=id).first()
        db.session.delete(person)
        db.session.commit()
        return True
    except Exception as e:
      print(e)
      return  False

```

Note that we have to use the `session.delete(person)` after we get the person by id, otherwise it will not work if we try to delete the person as follows:

```py
...
Person.query.filter_by(id=id).delete()
db.session.commit()
...
```

Now we are now able to make the following delete person mutation by passing the `id` of the person to the resolver.

```
mutation{
  deletePerson(id: 2)
}
```

If everything went well we will get the following response.

```json
{
  "data": {
    "deletePerson": true
  }
}
```

> Note that deleting this person will delete all the addresses related to this person.

**Note:**:

> To establish a `bidirectional` relationship in `one-to-many`, where the “reverse” side is a many to one, specify an additional `relationship()` and connect the two using the `relationship.back_populates` parameter.

Example from the [docs](https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many):

```py
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent", back_populates="children")
```

Note that `Many to One` relationship is just similar to `One to Many`.

### Many to One Relations

> Many to Many adds an `association` table between two classes. The association table is indicated by the relationship.secondary argument to `relationship()`. Usually, the Table uses the `MetaData` object associated with the declarative base class, so that the `ForeignKey` directives can locate the remote tables with which to link:

We are going to create a Question and Category models in the models package, where these two have a many to many relations to each other.

```py
...
questions_categories = db.Table('questions_categories',
    db.Column('question_id', db.Integer,
    db.ForeignKey('question.id'), primary_key=True),
    db.Column('category_id', db.Integer,
     db.ForeignKey('category.id'), primary_key=True)
)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(25), nullable=False)

    categories = db.relationship('Category', secondary=questions_categories, lazy='subquery',
        backref=db.backref('questions', lazy=True))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(25), nullable=False)

```

Note that the above is a unidirectional relationship. To make it bidirectional we change our models to look as follows:

```py
questions_categories = db.Table('questions_categories',
    db.Column('question_id', db.Integer,
    db.ForeignKey('question.id'), primary_key=True),
    db.Column('category_id', db.Integer,
     db.ForeignKey('category.id'), primary_key=True)
)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(25), nullable=False)

    categories = db.relationship('Category', secondary=questions_categories, lazy='subquery',
        backref=db.backref('questions', lazy=True),
        back_populates="questions")

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(25), nullable=False)
    questions = db.relationship('Category', secondary=questions_categories, lazy='subquery',
        backref=db.backref('categories', lazy=True),
        back_populates="categories")

```

### Creating a questions and categories.

We are going to allow users to create questions and then we add categories to the questions based on the question id provided. So in our `schema.graphql` we are going to add the following

```
schema {
  query: Query
  mutation: Mutation
}
....

type Category {
  id: Int!
  category: String!
}
type Question {
  id: Int!
  question: String!
  categories: [Category]!
}
..
type Query {
...
  getQuestion(id: Int): Question
  getQuestions: [Question]!
}

type Mutation {
...
  createCategory(category: String!, questionId: Int!): Category
  createQuestion(question: String!): Question
}

```

Then we will go to our mutation package and add the following resolvers that create questions and categories to questions

```py
def create_question_resolver(obj, info, question):
    try:
        qn = Question(question=question)
        db.session.add(qn)
        db.session.commit()
        return qn
    except Exception as e:
      return None

def create_category_resolver(obj, info, category, questionId):
    try:
        try:
            question = Question.query.filter_by(id=questionId).first()
        except:
            return {
                "category": None
            }

        cate = Category(category=category)
        db.session.add(cate)
        question.categories.append(cate)
        db.session.add(cate)
        db.session.commit()
        return cate
    except Exception as e:
      return None

```

We also want to have a functionality of getting all the questions and, also getting a question by id, we are going to to the queries package and add the following functions to it:

```py
def question_query_resolver(obj, info, id):
    try:
        question = Question.query.filter_by(id=id).first();
        return question
    except Exception as e:
        return None

def questions_query_resolver(obj, info):
    try:
        return Question.query.all();
    except Exception as e:
        return None
```

Now we can register our quiries and mutations in the `app.py` file.

So with this bare minimum code we will be able to make mutations and queries to our graphql api.

### Creating a Question

```
mutation {
  createQuestion(question: "how are you") {
    question
    id
    categories {
      id
      category
    }
  }
}

```

Response

```json
{
  "data": {
    "createQuestion": {
      "categories": [],
      "id": 7,
      "question": "how are you"
    }
  }
}
```

### Creating a category for our question of id `7`

Note that you can create as many categories as you want for a single question...

```
mutation {
  createCategory(category: "business", questionId: 7) {
    id
    category
  }
}

```

Response

```json
{
  "data": {
    "createCategory": {
      "category": "business",
      "id": 2
    }
  }
}
```

### Getting all the questions

```
{
  getQuestions {
    id
    question
    categories {
      category
      id
    }
  }
}

```

Response

```json
{
  "data": {
    "getQuestions": [
      {
        "categories": [],
        "id": 1,
        "question": "how are you"
      },
      {
        "categories": [],
        "id": 2,
        "question": "how are you"
      },
      {
        "categories": [],
        "id": 3,
        "question": "how are you"
      },
      {
        "categories": [],
        "id": 4,
        "question": "how are you"
      },
      {
        "categories": [],
        "id": 5,
        "question": "how are you"
      },
      {
        "categories": [],
        "id": 6,
        "question": "how are you"
      },
      {
        "categories": [
          {
            "category": "sport",
            "id": 1
          }
        ],
        "id": 7,
        "question": "how are you"
      }
    ]
  }
}
```

### Getting a single question

```
{
  getQuestion(id: 7) {
    id
    question
    categories {
      category
      id
    }
  }
}

```

Response:

```json
{
  "data": {
    "getQuestion": {
      "categories": [
        {
          "category": "sport",
          "id": 1
        },
        {
          "category": "business",
          "id": 2
        }
      ],
      "id": 7,
      "question": "how are you"
    }
  }
}
```

### Deleting a many to many relationship according to the [docs](https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#deleting-rows-from-the-many-to-many-table)

> A behavior which is unique to the relationship.secondary argument to relationship() is that the Table which is specified here is automatically subject to INSERT and DELETE statements, as objects are added or removed from the collection. There is no need to delete from this table manually. The act of removing a record from the collection will have the effect of the row being deleted on flush:

```py
myparent.children.remove(somechild)
```

### References

1. [ariadnegraphql](https://ariadnegraphql.org/docs/)
2. [sqlalchemy.org](https://docs.sqlalchemy.org)
3. [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/)
