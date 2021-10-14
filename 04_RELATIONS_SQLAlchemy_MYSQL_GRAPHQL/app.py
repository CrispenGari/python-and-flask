from api import app, db
from ariadne import QueryType, MutationType, load_schema_from_path, make_executable_schema, graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify

from api.resolvers.mutations import create_category_resolver, create_email_addresses, create_person_resolver, create_profile_resolver, create_question_resolver, delete_person_resolver, register_user_resolver, update_email_addresses
from api.resolvers.queries import person_query_resolver, question_query_resolver, questions_query_resolver, user_resolver

query = QueryType()
mutation = MutationType()

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation
)

# Mutations
mutation.set_field("register", register_user_resolver)
mutation.set_field("createProfile", create_profile_resolver)

mutation.set_field("createAddress", create_email_addresses)
mutation.set_field("createPerson", create_person_resolver)
mutation.set_field("deletePerson", delete_person_resolver)
mutation.set_field("updateAddress", update_email_addresses)


mutation.set_field("createCategory", create_category_resolver)
mutation.set_field("createQuestion", create_question_resolver)

# Queries
query.set_field("user", user_resolver)
query.set_field("getPerson", person_query_resolver)


query.set_field("getQuestions", questions_query_resolver)
query.set_field("getQuestion", question_query_resolver)


type_defs = load_schema_from_path("schema.graphql")

# Schema
schema = make_executable_schema(
    type_defs, mutation, query
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
    db.create_all()
    app.run(debug=True, port=3001)