from api import app, db
from ariadne import QueryType, MutationType, load_schema_from_path, make_executable_schema, graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify

from api.mutation import create_post_resolver, delete_post_resolver, update_post_resolver
from api.queries import get_post_resolver, get_posts_resolver

query = QueryType()
mutation = MutationType()


# Queries
query.set_field("getPosts", get_posts_resolver)
query.set_field("getPost", get_post_resolver)

# Mutations
mutation.set_field("createPost", create_post_resolver)
mutation.set_field("updatePost", update_post_resolver)
mutation.set_field("deletePost", delete_post_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation
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
    # db.create_all()
    app.run(debug=True, port=3001)
