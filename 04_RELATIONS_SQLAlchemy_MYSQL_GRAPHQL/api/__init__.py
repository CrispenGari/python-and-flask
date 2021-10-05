
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from ariadne import QueryType, MutationType, load_schema_from_path, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML

from api.resolvers.mutations import register_user_resolver

query = QueryType()
mutation = MutationType()

mutation.set_field("register", register_user_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, mutation
)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/relations"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)

db = SQLAlchemy(app)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

# @app.route("/graphql", methods=["POST"])
# def graphql_server():
#     data = request.get_json()
#     success, result = graphql_sync(
#         schema,
#         data,
#         context_value=request,
#         debug=True
#     )
#     status_code = 200 if success else 400
#     return jsonify(result), status_code
