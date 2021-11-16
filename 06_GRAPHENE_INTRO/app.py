from flask_graphql import GraphQLView
from schema import schema
from api import app, db


app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,

))

if __name__ == '__main__':
    db.create_all()
    app.run(port=3001, debug=True)