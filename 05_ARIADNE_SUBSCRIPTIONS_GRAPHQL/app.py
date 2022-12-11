from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLWSHandler
from starlette.applications import Starlette
from api.pubsub import pubsub
from api.resolvers.mutations import mutation
from api.resolvers.subscriptions import subscription
from api.resolvers.queries import query

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(type_defs, [query, mutation, subscription])
graphql = GraphQL(
    schema=schema,
    debug=True,
    websocket_handler=GraphQLWSHandler(),
)

app = Starlette(
    debug=True,
    on_startup=[pubsub.connect],
    on_shutdown=[pubsub.disconnect],
)

app.mount("/graphql", graphql)