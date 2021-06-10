from keys.keys import pwd
import pymongo
from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse, marshal_with, fields

"""
DATABASE CONFIGURATION
"""

databaseName = "students"
connection_url = f'mongodb+srv://crispen:{pwd}@cluster0.3zay8.mongodb.net/{databaseName}?retryWrites=true&w=majority'
client = pymongo.MongoClient(connection_url)
cursor = client.list_database_names()
db = client.blob

"""
Student post args
"""
student_post_args = reqparse.RequestParser()
student_post_args.add_argument("name", type=str, help="name required", required=True)
student_post_args.add_argument("surname", type=str, help="surname required", required=True)
student_post_args.add_argument("student_number", type=int, help="student number required", required=True)
student_post_args.add_argument("course", type=str, help="name required", required=True)
student_post_args.add_argument("mark", type=int, help="surname required", required=True)

"""
Student patch args
    * We want to be able only to update student course and mark
"""

"""
Resource Fields
"""
resource_fields = {
    '_id': fields.String,
	'name': fields.String,
	'surname': fields.String,
	'course': fields.String,
	'mark': fields.Integer,
    "student_number":fields.Integer,
}

app = Flask(__name__)
app.config["ENV"] = "development"
api = Api(app)

class GetPatchDeleteStudent(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        cursor = db.students.find_one({"student_number": id})
        if cursor is None:
            abort(404, f"Student with student number {id} not found.")
        return cursor, 200

    def delete(self, id):
        cursor = db.students.find_one({"student_number": id})
        if cursor is None:
            abort(404, f"Student with student number {id} not found.")
        
        db.students.delete_one({"student_number": id})
        return "", 204

    @marshal_with(resource_fields)
    def patch(self, id):
        args = student_post_args.parse_args()
        cursor = db.students.find_one({"student_number": id})
        if cursor is None:
            abort(404, f"Student with student number {id} not found.")

        if args["mark"]:
            db.students.update_one({"student_number": id}, {"$set":
                {"mark": args["mark"]}
            })
        if args["course"]:
            db.students.update_one({"student_number": id}, {
                "$set": {"course": args["course"]}
            })
        return db.students.find_one({"student_number": id}), 204
    
class PostStudent(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = student_post_args.parse_args()
        cursor = db.students.find_one({"student_number": args["student_number"]})
        if cursor is None:
            """
            Insert the students to the database.
            """
            res = db.students.insert_one({
                "name": args["name"],
                "surname": args["surname"],
                "student_number": args["student_number"],
                "course": args["course"],
                "mark": args["mark"]
            })
            print(res, type(res))
        else:
            abort(409, "Student number taken by another student")
        return db.students.find_one({"student_number": args["student_number"]}), 201

api.add_resource(PostStudent, '/student')
api.add_resource(GetPatchDeleteStudent, '/student/<int:id>')

if __name__ == "__main__":
    app.run(debug=True)