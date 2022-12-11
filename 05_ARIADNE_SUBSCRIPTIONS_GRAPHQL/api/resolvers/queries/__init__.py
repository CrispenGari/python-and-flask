from ariadne import QueryType
query = QueryType()

@query.field("hello")
def hello_resolver(obj, info, username):
    return f"Hello, {username}"