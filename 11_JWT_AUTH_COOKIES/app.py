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
    def decorated_function(self, *args, **kws):
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
                return f(self, res, *args, **kws) 
            except Exception as e:
                res= make_response(jsonify({
                    'code': '401',
                    'message': 'Invalid token or it has expired.',
                    'timestamp': datetime.now(),
                 }), 401)
                return f(self, res, *args, **kws) 
        else:
            res = make_response(jsonify({
                'code': '401',
                'message': 'You need to be authenticated.',
                'timestamp': datetime.now(),
            }), 401)
            return f(self, res, *args, **kws)        
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