### Ariadne Subscriptions

In this repository I will show how we can perform graphql-subscriptions using `ariadne`

### Installing websockets

First of all you need to install required packages by running the following command

```shell
pip install ariadne uvicorn
```

### Setting Up the server

In the `app.py` we are going to have the following code:

```py
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
```

Our `schema.graphql` looks as follows:

```graphql
schema {
  query: Query
  mutation: Mutation
  subscription: Subscription
}

type Query {
  hello(username: String!): String!
}

type Mutation {
  sendMessage(message: String!): String!
}

type Subscription {
  newMessage: String!
}
```

Our subscription will look as follows:

```py
from api.pubsub import pubsub
from ariadne import SubscriptionType
subscription = SubscriptionType()

@subscription.source("newMessage")
async def source_message(_, info):
    async with pubsub.subscribe(channel="message") as subscriber:
        async for event in subscriber:
            yield event.message
```

Our Mutation will look as follows:

```py
from api.pubsub import pubsub
from ariadne import MutationType
mutation = MutationType()

@mutation.field("sendMessage")
async def sendMessage_resolver(obj, info, message):
    await pubsub.publish(channel="message", message=message)
    return message
```

The `pubsub` will come from the `api.pubsub` object and it looks as follows:

```py
from broadcaster import Broadcast
pubsub = Broadcast("memory://")
```

### Running the server

Now that our app is ready we can go ahead and run it as follows:

```shell
uvicorn app:app
```

### Ref

1. [ariadnegraphql.org](https://ariadnegraphql.org/docs/subscriptions.html)
2. [twilio blog](https://www.twilio.com/blog/graphql-api-subscriptions-python-asyncio-ariadne)
