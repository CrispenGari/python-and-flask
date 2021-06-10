### MongoDB REST + Flask

In this README we are going to Create a simple rest API application for students marks using the cloud mongodb. If you need more information about how to connect to mongodb cloud database [here](https://github.com/CrispenGari/python-and-mongodb) is the help. In this notebook we will just focusing on python code and make everything work.

### Installation

To install the driver that will help us to interact with mongodb `pymongo` we run the following command.

```shell
pip install pymongo

pip install dnspython
```

Go ahead and create an mongodb application [here](https://www.mongodb.com/cloud/atlas/lp/try2?utm_source=google&utm_campaign=gs_emea_south_africa_search_core_brand_atlas_desktop&utm_term=mongodb&utm_medium=cpc_paid_search&utm_ad=e&utm_ad_campaign_id=12212624560&gclid=CjwKCAjwvMqDBhB8EiwA2iSmPCap41KoEEBRMXvy2shU7erYMPtg6oZe14eG04B_vdW6w6o1hdWYBBoCVIwQAvD_BwE).

### THE WHOLE CODE IN THE `main.py`.

```py
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

```

This code allows us to add, delete, update and get a student from mongodb database. The code is self explanatory all you need is the knowledge from the previous README as well as the knowledge of pymongo.
