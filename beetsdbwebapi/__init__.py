from flask import (Flask,
                   jsonify,
                   abort,
                   make_response,
                   request)
from flask_graphql import GraphQLView
from beetsdbwebapi.models import db_session
from beetsdbwebapi.schema import schema

app = Flask(__name__)

app.add_url_rule('/graphql',
                 view_func=GraphQLView.as_view('graphql',
                                               schema=schema,
                                               graphiql=True))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True)
