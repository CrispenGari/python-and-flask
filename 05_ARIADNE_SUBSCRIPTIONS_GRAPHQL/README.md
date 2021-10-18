### Ariadne and SqlAlchemy GraphQL subscriptions

> This is where the `Subscription` type is useful. It's similar to `Query` but as each subscription remains an open channel you can send anywhere from zero to millions of responses over its lifetime.

### Installing websockets

> Because of their nature, subscriptions are only possible to implement in asynchronous servers that implement the WebSockets protocol. - Docs.

```shell
pip install websockets
```

### Ref

1. [ariadnegraphql.org](https://ariadnegraphql.org/docs/subscriptions.html)
2. [twilio blog](https://www.twilio.com/blog/graphql-api-subscriptions-python-asyncio-ariadne)
