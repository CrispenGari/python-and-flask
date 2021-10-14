from api import app, db
from ariadne import SubscriptionType, load_schema_from_path, make_executable_schema, graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from api.resolvers.mutations import mutation
from api.resolvers.queries import query

subscription = SubscriptionType()


type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, subscription
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
    return jsonify(result), 200 if success else 400

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=3001)