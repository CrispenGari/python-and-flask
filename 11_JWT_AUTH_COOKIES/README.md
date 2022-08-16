### Authentication JWT and Cookies

In this practical we are going to learn how we can do authentication with `jwt` and cookies in flask. Basically we are going to create an authentication API.

### Installing of packages:

We are going to install the following packages:

```shell

pip install flask pyjwt Flask-SQLAlchemy argon2-cffi
```

### User Model

First we are going to create a model called users which will look as follows:

```py
from app import db

class User(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120),  nullable=False, unique=True)
    password = db.Column(db.String(500),  nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, username, email,  password):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'updated_at': self.updated_at,
            'created_at': self.created_at,
        }

# create the tables
db.create_all()
```

This is a simple model that allows us to store the information of the user. Our `app` package has the following code in it.

```py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
app = Flask(__name__)
app.secret_key = "abcd"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=7)
db = SQLAlchemy(app)
```

### Registering the user

To register the user we are going to do the following:

1. create a new user and save in the database
2. store the `{username, id}` of the user in the `jwt` token
3. create a cookie `jwt` and save the token.

THe route for doing that is as follows:

```py
@app.route('/register', methods=["POST"])
def register():
    if request.method == "POST":
        if request.is_json:
            try:
                data = request.get_json()
                hashedPassword = hasher.hash(data.get('password'))
                user = User(data.get('username'), data.get('email'), hashedPassword)
                db.session.add(user)
                db.session.commit()
                # Put the token into the session
                payload ={
                    'id': user.id,
                    'username': user.username
                }
                token = jwt.encode(payload, SECRETE, algorithm="HS256")

                res = make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 201,
                    'message': "User created.",
                    'user': user.to_json()
                 }), 201)
                res.set_cookie(
                    TOKEN_KEY,
                    token,
                    timedelta(days=3),
                    samesite="Lax"
                )
                return res
            except Exception as e:
                return make_response(jsonify({
                    'code': '500',
                    'message': str(e),
                    'timestamp': datetime.now(),
                }), 500)
        else:
           return make_response(jsonify({
            'code': '500',
            'message': 'Json data allowed.',
            'timestamp': datetime.now(),
            }), 500)
    else:
        return make_response(jsonify({
            'code': '405',
            'message': 'Method not allowed.',
            'timestamp': datetime.now(),
            }), 405)
```

So we send a `POST` request to `http://localhost:3001/register` with the following json data:

```json
{
  "username": "crispengari",
  "email": "crispengari@gmail.com",
  "password": "crispengari"
}
```

The user will be created.

### Logging out the user

To logout the user we are going to do the following:

1. delete the cookie `jwt`

The route for doing that is as follows:

```py
@app.route('/logout', methods=["POST"])
def logout():
    if request.method == "POST":
        # logout

        res =  make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 200,
                    'message': "Logged Out.",
                    'user': None
                }), 200)
        res.delete_cookie(TOKEN_KEY)
        return res
    else:
        return make_response(jsonify({
            'code': '405',
            'message': 'Method not allowed.',
            'timestamp': datetime.now(),
            }), 405)
```

So we send a `POST` request to `http://localhost:3001/logout` and we will get the following response:

```json
{
  "code": 200,
  "message": "Logged Out.",
  "timestamp": "Tue, 16 Aug 2022 10:21:29 GMT",
  "user": null
}
```

### Login the user

To log in the user we do the following step:

1. get the user from the database using email or password
2. if we get it we are going to verify the plain password with the hashed password in the database.
3. if we succeed we are going to store the payload with `{username, id}` in the `jwt` token.
4. then finally we store the cookie with a key `jwt`

The route for doing that is as follows:

```py
@app.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        if request.is_json:
            try:
                data = request.get_json()
                user = User.query.filter_by(username=data.get('usernameOrEmail')).first()
                user = user if user else User.query.filter_by(email=data.get('usernameOrEmail')).first()
                if user:
                    # login
                    # create a jwt token and store it in a cookie
                    try:
                        hasher.verify(user.password, data.get('password'))
                        payload ={
                            'id': user.id,
                            'username': user.username
                        }
                        token = jwt.encode(payload, SECRETE, algorithm="HS256")
                        res =  make_response(jsonify({
                            'timestamp': datetime.now(),
                            'code': 200,
                            'message': "Logged in.",
                            'user': user.to_json()
                        }), 200)
                        res.set_cookie(
                            TOKEN_KEY,
                            token,
                            timedelta(days=3),
                            samesite="Lax"
                        )
                        return res
                    except Exception as e:
                        return make_response(jsonify({
                            'timestamp': datetime.now(),
                            'code': 200,
                            'message':  str(e),
                            'user': None
                        }), 200)
                else:
                    return  make_response(jsonify({
                        'timestamp': datetime.now(),
                        'code': 200,
                        'message': "Invalid credentials.",
                        'user': None
                 }), 200)
            except Exception as e:
                return make_response(jsonify({
                    'code': '500',
                    'message': str(e),
                    'timestamp': datetime.now(),
                }), 500)
        else:
           return make_response(jsonify({
            'code': '500',
            'message': 'Json data allowed.',
            'timestamp': datetime.now(),
            }), 500)
    else:
        return make_response(jsonify({
            'code': '405',
            'message': 'Method not allowed.',
            'timestamp': datetime.now(),
            }), 405)
```

So to login you need to send a `POST` request to `http://127.0.0.1:3001/login` with the payload that looks as follows:

```json
{
  "usernameOrEmail": "crispengari",
  "password": "crispengari"
}
```

On success login you will get the following json response

```json
{
  "code": 200,
  "message": "Logged in.",
  "timestamp": "Tue, 16 Aug 2022 10:26:20 GMT",
  "user": {
    "created_at": "Tue, 16 Aug 2022 08:15:13 GMT",
    "email": "crispengari@gmail.com",
    "id": 3,
    "updated_at": "Tue, 16 Aug 2022 08:15:13 GMT",
    "username": "crispengari"
  }
}
```

### Getting the authenticated user.

To get the authenticated user we are going to do the following:

1. get the token from the cookies
2. decode the jwt token and get a payload
3. then we will get the user from the database based on the id in the payload

The route for doing that is as follows:

```py

@app.route('/user', methods=["GET"])
def user():
    if request.method == "GET":
        cookies = dict(request.cookies)
        token = cookies.get(TOKEN_KEY)
        if token:
            try:
                payload = jwt.decode(token, SECRETE, algorithms=["HS256"])
                user = User.query.filter_by(id=payload.get('id')).first()
                res =  make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 200,
                    'message': "User.",
                    'user': user.to_json()
                }), 200)
                return res
            except Exception as e:
                print(e)
                return make_response(jsonify({
                    'code': '401',
                    'message': 'Invalid token or it has expired.',
                    'timestamp': datetime.now(),
                 }), 401)
        else:
            return make_response(jsonify({
                'code': '401',
                'message': 'You need to be authenticated.',
                'timestamp': datetime.now(),
            }), 401)
    else:
        return make_response(jsonify({
            'code': '405',
            'message': 'Method not allowed.',
            'timestamp': datetime.now(),
            }), 405)


```

To get the user you just need to send a `GET` request to `http://127.0.0.1:3001/user` if you are logged in you get the following response:

```json
{
  "code": 200,
  "message": "User.",
  "timestamp": "Tue, 16 Aug 2022 10:30:46 GMT",
  "user": {
    "created_at": "Tue, 16 Aug 2022 08:15:13 GMT",
    "email": "crispengari@gmail.com",
    "id": 3,
    "updated_at": "Tue, 16 Aug 2022 08:15:13 GMT",
    "username": "crispengari"
  }
}
```

If not you get the following response:

```json
{
  "code": "401",
  "message": "You need to be authenticated.",
  "timestamp": "Tue, 16 Aug 2022 10:32:15 GMT"
}
```

### Protecting Routes and Authorizing.

In this section we are going to create a function decorator that will protect the `home` route. It will check if the user is authenticated or not based on the token that is stored in the `cookies`. The `authorize` decorated function looks as follows.

```py
def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        cookies = dict(request.cookies)
        token = cookies.get(TOKEN_KEY)
        if token:
            try:
                payload = jwt.decode(token, SECRETE, algorithms=["HS256"])
                user = User.query.filter_by(id=payload.get('id')).first()
                res =  make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 200,
                    'message': "User.",
                    'user': user.to_json()
                }), 200)
                return f(res, *args, **kws)
            except Exception as e:
                res= make_response(jsonify({
                    'code': '401',
                    'message': 'Invalid token or it has expired.',
                    'timestamp': datetime.now(),
                 }), 401)
                return f(res, *args, **kws)
        else:
            res = make_response(jsonify({
                'code': '401',
                'message': 'You need to be authenticated.',
                'timestamp': datetime.now(),
            }), 401)
            return f(res, *args, **kws)
    return decorated_function
```

Now to protect the '/' route we are going to decorate our `home` route as follows:

```py
@app.route('/', methods=["GET"])
@authorize
def home(res):
    return res
```

If you are not logged in when you try to access `http://127.0.0.1:3001/` you get the following response:

```json
{
  "code": "401",
  "message": "You need to be authenticated.",
  "timestamp": "Tue, 16 Aug 2022 10:40:53 GMT"
}
```

Otherwise you get the following response

```json
{
  "code": 200,
  "message": "User.",
  "timestamp": "Tue, 16 Aug 2022 10:46:02 GMT",
  "user": {
    "created_at": "Tue, 16 Aug 2022 08:15:13 GMT",
    "email": "crispengari@gmail.com",
    "id": 3,
    "updated_at": "Tue, 16 Aug 2022 08:15:13 GMT",
    "username": "crispengari"
  }
}
```

### Functional Based Views

The function based views of this `API` looks as follows

```py
from flask import make_response, request, jsonify
from app import app, db
from argon2 import PasswordHasher
from datetime import datetime, timedelta
from models import User
import jwt
from functools import wraps

hasher = PasswordHasher(salt_len=12)
SECRETE = 'dfghjkla56789okmnbdfgh9no12uw6dcvbnnnmo'
TOKEN_KEY = 'jwt'

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        cookies = dict(request.cookies)
        token = cookies.get(TOKEN_KEY)
        if token:
            try:
                payload = jwt.decode(token, SECRETE, algorithms=["HS256"])
                user = User.query.filter_by(id=payload.get('id')).first()
                res =  make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 200,
                    'message': "User.",
                    'user': user.to_json()
                }), 200)
                return f(res, *args, **kws)
            except Exception as e:
                res= make_response(jsonify({
                    'code': '401',
                    'message': 'Invalid token or it has expired.',
                    'timestamp': datetime.now(),
                 }), 401)
                return f(res, *args, **kws)
        else:
            res = make_response(jsonify({
                'code': '401',
                'message': 'You need to be authenticated.',
                'timestamp': datetime.now(),
            }), 401)
            return f(res, *args, **kws)


    return decorated_function


@app.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        if request.is_json:
            try:
                data = request.get_json()
                user = User.query.filter_by(username=data.get('usernameOrEmail')).first()
                user = user if user else User.query.filter_by(email=data.get('usernameOrEmail')).first()
                if user:
                    # login
                    # create a jwt token and store it in a cookie
                    try:
                        hasher.verify(user.password, data.get('password'))
                        payload ={
                            'id': user.id,
                            'username': user.username
                        }
                        token = jwt.encode(payload, SECRETE, algorithm="HS256")
                        res =  make_response(jsonify({
                            'timestamp': datetime.now(),
                            'code': 200,
                            'message': "Logged in.",
                            'user': user.to_json()
                        }), 200)
                        res.set_cookie(
                            TOKEN_KEY,
                            token,
                            timedelta(days=3),
                            samesite="Lax"
                        )
                        return res
                    except Exception as e:
                        return make_response(jsonify({
                            'timestamp': datetime.now(),
                            'code': 200,
                            'message':  str(e),
                            'user': None
                        }), 200)
                else:
                    return  make_response(jsonify({
                        'timestamp': datetime.now(),
                        'code': 200,
                        'message': "Invalid credentials.",
                        'user': None
                 }), 200)
            except Exception as e:
                return make_response(jsonify({
                    'code': '500',
                    'message': str(e),
                    'timestamp': datetime.now(),
                }), 500)
        else:
           return make_response(jsonify({
            'code': '500',
            'message': 'Json data allowed.',
            'timestamp': datetime.now(),
            }), 500)
    else:
        return make_response(jsonify({
            'code': '405',
            'message': 'Method not allowed.',
            'timestamp': datetime.now(),
            }), 405)

@app.route('/register', methods=["POST"])
def register():
    if request.method == "POST":
        if request.is_json:
            try:
                data = request.get_json()
                hashedPassword = hasher.hash(data.get('password'))
                user = User(data.get('username'), data.get('email'), hashedPassword)
                db.session.add(user)
                db.session.commit()
                # Put the token into the session
                payload ={
                    'id': user.id,
                    'username': user.username
                }
                token = jwt.encode(payload, SECRETE, algorithm="HS256")

                res = make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 201,
                    'message': "User created.",
                    'user': user.to_json()
                 }), 201)
                res.set_cookie(
                    TOKEN_KEY,
                    token,
                    timedelta(days=3),
                    samesite="Lax"
                )
                return res
            except Exception as e:
                return make_response(jsonify({
                    'code': '500',
                    'message': str(e),
                    'timestamp': datetime.now(),
                }), 500)
        else:
           return make_response(jsonify({
            'code': '500',
            'message': 'Json data allowed.',
            'timestamp': datetime.now(),
            }), 500)
    else:
        return make_response(jsonify({
            'code': '405',
            'message': 'Method not allowed.',
            'timestamp': datetime.now(),
            }), 405)

@app.route('/user', methods=["GET"])
def user():
    if request.method == "GET":
        cookies = dict(request.cookies)
        token = cookies.get(TOKEN_KEY)
        if token:
            try:
                payload = jwt.decode(token, SECRETE, algorithms=["HS256"])
                user = User.query.filter_by(id=payload.get('id')).first()
                res =  make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 200,
                    'message': "User.",
                    'user': user.to_json()
                }), 200)
                return res
            except Exception as e:
                print(e)
                return make_response(jsonify({
                    'code': '401',
                    'message': 'Invalid token or it has expired.',
                    'timestamp': datetime.now(),
                 }), 401)
        else:
            return make_response(jsonify({
                'code': '401',
                'message': 'You need to be authenticated.',
                'timestamp': datetime.now(),
            }), 401)
    else:
        return make_response(jsonify({
            'code': '405',
            'message': 'Method not allowed.',
            'timestamp': datetime.now(),
            }), 405)


@app.route('/logout', methods=["POST"])
def logout():
    if request.method == "POST":
        # logout

        res =  make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 200,
                    'message': "Logged Out.",
                    'user': None
                }), 200)
        res.delete_cookie(TOKEN_KEY)
        return res
    else:
        return make_response(jsonify({
            'code': '405',
            'message': 'Method not allowed.',
            'timestamp': datetime.now(),
            }), 405)

@app.route('/', methods=["GET"])
@authorize
def home(res):
    return res




if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=3001, host='127.0.0.1') # allow hot reloading
```

### The Class based version looks as follows

```py
from flask import make_response, request, jsonify, views
from app import app, db
from argon2 import PasswordHasher
from datetime import datetime, timedelta
from models import User
import jwt
from functools import wraps

hasher = PasswordHasher(salt_len=12)
SECRETE = 'dfghjkla56789okmnbdfgh9no12uw6dcvbnnnmo'
TOKEN_KEY = 'jwt'

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        cookies = dict(request.cookies)
        token = cookies.get(TOKEN_KEY)
        if token:
            try:
                payload = jwt.decode(token, SECRETE, algorithms=["HS256"])
                user = User.query.filter_by(id=payload.get('id')).first()
                res =  make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 200,
                    'message': "User.",
                    'user': user.to_json()
                }), 200)
                return f(res, *args, **kws)
            except Exception as e:
                res= make_response(jsonify({
                    'code': '401',
                    'message': 'Invalid token or it has expired.',
                    'timestamp': datetime.now(),
                 }), 401)
                return f(res, *args, **kws)
        else:
            res = make_response(jsonify({
                'code': '401',
                'message': 'You need to be authenticated.',
                'timestamp': datetime.now(),
            }), 401)
            return f(res, *args, **kws)
    return decorated_function



class Auth(views.MethodView):
    def get(self):
        cookies = dict(request.cookies)
        token = cookies.get(TOKEN_KEY)
        if token:
            try:
                payload = jwt.decode(token, SECRETE, algorithms=["HS256"])
                user = User.query.filter_by(id=payload.get('id')).first()
                res =  make_response(jsonify({
                    'timestamp': datetime.now(),
                    'code': 200,
                    'message': "User.",
                    'user': user.to_json()
                }), 200)
                return res
            except Exception as e:
                print(e)
                return make_response(jsonify({
                    'code': '401',
                    'message': 'Invalid token or it has expired.',
                    'timestamp': datetime.now(),
                 }), 401)
        else:
            return make_response(jsonify({
                'code': '401',
                'message': 'You need to be authenticated.',
                'timestamp': datetime.now(),
            }), 401)

    def post(self):
        if request.path == '/login':
            if request.is_json:
                try:
                    data = request.get_json()
                    user = User.query.filter_by(username=data.get('usernameOrEmail')).first()
                    user = user if user else User.query.filter_by(email=data.get('usernameOrEmail')).first()
                    if user:
                        # login
                        # create a jwt token and store it in a cookie
                        try:
                            hasher.verify(user.password, data.get('password'))
                            payload ={
                                'id': user.id,
                                'username': user.username
                            }
                            token = jwt.encode(payload, SECRETE, algorithm="HS256")
                            res =  make_response(jsonify({
                                'timestamp': datetime.now(),
                                'code': 200,
                                'message': "Logged in.",
                                'user': user.to_json()
                            }), 200)
                            res.set_cookie(
                                TOKEN_KEY,
                                token,
                                timedelta(days=3),
                                samesite="Lax"
                            )
                            return res
                        except Exception as e:
                            return make_response(jsonify({
                                'timestamp': datetime.now(),
                                'code': 200,
                                'message':  str(e),
                                'user': None
                            }), 200)
                    else:
                        return  make_response(jsonify({
                            'timestamp': datetime.now(),
                            'code': 200,
                            'message': "Invalid credentials.",
                            'user': None
                    }), 200)
                except Exception as e:
                    return make_response(jsonify({
                        'code': '500',
                        'message': str(e),
                        'timestamp': datetime.now(),
                    }), 500)
            else:
                return make_response(jsonify({
                    'code': '500',
                    'message': 'Json data allowed.',
                    'timestamp': datetime.now(),
                    }), 500)

        elif request.path == '/logout':
            res =  make_response(jsonify({
                'timestamp': datetime.now(),
                'code': 200,
                'message': "Logged Out.",
                'user': None
            }), 200)
            res.delete_cookie(TOKEN_KEY)
            return res

        elif request.path == '/register':
            if request.is_json:
                try:
                    data = request.get_json()
                    hashedPassword = hasher.hash(data.get('password'))
                    user = User(data.get('username'), data.get('email'), hashedPassword)
                    db.session.add(user)
                    db.session.commit()
                    # Put the token into the session
                    payload ={
                        'id': user.id,
                        'username': user.username
                    }
                    token = jwt.encode(payload, SECRETE, algorithm="HS256")

                    res = make_response(jsonify({
                        'timestamp': datetime.now(),
                        'code': 201,
                        'message': "User created.",
                        'user': user.to_json()
                    }), 201)
                    res.set_cookie(
                        TOKEN_KEY,
                        token,
                        timedelta(days=3),
                        samesite="Lax"
                    )
                    return res
                except Exception as e:
                    return make_response(jsonify({
                        'code': '500',
                        'message': str(e),
                        'timestamp': datetime.now(),
                    }), 500)
            else:
              return make_response(jsonify({
                'code': '500',
                'message': 'Json data allowed.',
                'timestamp': datetime.now(),
                }), 500)

        else:
            return make_response(jsonify({
                'code': '404',
                'message': f'Path "{request.path}" not found.',
                'timestamp': datetime.now(),
            }), 404)

class App(views.MethodView):
    decorators = [authorize]

    def get(self, res):
        print(res)
        return jsonify({'hello': 1})


auth_view = Auth.as_view('auth')
app_view = App.as_view('app')

app.add_url_rule('/login', methods=['POST'], view_func=auth_view)
app.add_url_rule('/logout', methods=['POST'], view_func=auth_view)
app.add_url_rule('/register', methods=['POST'], view_func=auth_view)
app.add_url_rule('/user', methods=['GET'], view_func=auth_view)
app.add_url_rule('/', methods=['GET'], view_func=app_view)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=3001, host='127.0.0.1') # allow hot reloading
```

### Ref

1. [pyjwt.readthedocs.io](https://pyjwt.readthedocs.io/en/stable/)
2. [argon2-cffi](https://pypi.org/project/argon2-cffi/)
