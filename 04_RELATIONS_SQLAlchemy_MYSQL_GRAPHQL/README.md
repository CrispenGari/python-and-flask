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

We are then going to create two models in the `models` package. The first model will be in its own package `user` and the code looks as follows:

```py

from api import db
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    userId = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    profile = db.relationship('profile', backref='profiles', lazy=True)

    def __repr__(self) -> str:
        return '<User %r>' % self.username

    def to_dict(self):
         return {
            "userId": str(self.userId),
            "username": self.username,
            "profile": self.profile.to_dict()
        }
```

The `profile` model will be in the profile package and the code looks as follows:

```py
from api import db
class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    profileId = db.Column(db.String(50), nullable=False, unique=True)
    gender = db.Column(db.String(15), nullable=False, unique=True)
    userId = db.Column(db.String(50), db.ForeignKey('users.userId'),
        nullable=False)

    def __repr__(self) -> str:
        return '<Profile %r>' % self.profileId

    def to_dict(self):
         return {
            "userId": str(self.userId),
            "profileId": self.profileId,
            "gender": self.gender
        }
```

Now we have a `one-to-one` `bidirectional` relationship between the `user` and his `profile`.

### GraphQL Schema

Next we are going to create our graphql schema so that we will be able to persist the user's infomation in the database using graphql resolvers.
