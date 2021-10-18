from api import app, db
from ariadne import  load_schema_from_path, make_executable_schema, graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from api.resolvers.subscriptions import subscription
from api.resolvers.mutations import mutation
from api.resolvers.queries import query
from ariadne.asgi import GraphQL
from starlette.routing import Route, WebSocketRoute

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, subscription
)


# routers = [
#     Route("/graphql", GraphQL(schema=schema, debug=True)),

#     WebSocketRoute("/graphql", GraphQL(schema=schema, debug=True)),
# ]
# app = Starlette(debug=True, routes=routers)


app.root_path= routers

@app.route("/", methods=["GET"], )
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/", methods=["POST"])
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
    app.run(debug=True, port=3001 )