from flask import Flask, abort
from flask_restful import Api, Resource, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["ENV"] = "development"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
api = Api(app)

"""
Args for posting the data 
"""
user_post_args = reqparse.RequestParser()
user_post_args.add_argument("username", type=str, help="Username required", required=True)
user_post_args.add_argument("likes", type=int, help="Like required", required=True)
user_post_args.add_argument("comments", type=int, help="Comments required", required=True)

"""
Args for updating the data (These field must not be required.)
"""
user_patch_args = reqparse.RequestParser()
user_patch_args.add_argument("username", type=str, help="Username required")
user_patch_args.add_argument("likes", type=int, help="Like required")
user_patch_args.add_argument("comments", type=int, help="Comments required")

"""
Resource Fields
"""
resource_fields = {
    'id': fields.Integer,
	'username': fields.String,
	'comments': fields.Integer,
	'likes': fields.Integer
}

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True, nullable=False)
    username = db.Column("username", db.String(25), nullable=False)
    likes = db.Column("likes", db.Integer, nullable=False)
    comments = db.Column("comments", db.Integer, nullable=False)

    def __init__(self, id, username, likes, comments):
        self.id = id
        self.username = username
        self.likes = likes
        self.comments = comments

    def __repr__(self):
        return f"[username: {self.username}, id: {self.id}, likes: {self.likes}, comments: {self.comments}]"

# db.create_all()
profiles = {}
class Profile(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        result = User.query.filter_by(id=id).first()
        if not result:
            abort(404, "User not found.")
        return result, 200

    @marshal_with(resource_fields)
    def post(self, id):
        args = user_post_args.parse_args()
        """
        Check if the profile exists if not exist create 1 if exist 
        return an error using abort()
        """
        result = User.query.filter_by(id=id).first()
        if result:
            abort(409, "User already exists.")
        user = User(id=id, username= args['username'], likes=args['likes'], comments=args['comments'])
        db.session.add(user)
        db.session.commit()
        return user, 201 # status code for created 

    def delete(self, id):
        result = User.query.filter_by(id=id).first()
        if not result:
            abort(404, "User does not exist.")
        
        db.session.delete(result)
        db.session.commit()
        return "User deleted", 204 # status code for deleted

    @marshal_with(resource_fields)
    def patch(self, id):
        args = user_patch_args.parse_args()
        result = User.query.filter_by(id=id).first()

        if result:
            if args['username']:
                result.username = args['username']
            if args['likes']:
                result.likes = args['likes']
            if args['comments']:
                result.comments = args['comments']
            db.session.commit()
        else:
            abort(404, "Failed to update, user not found")
        # save updates
        return args, 204    
api.add_resource(Profile, '/user/<int:id>')
if __name__ == "__main__":
    app.run(debug=True)