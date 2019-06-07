from flask import Flask, jsonify, abort, make_response, request
from flask_graphql import GraphQLView
from beetsdbwebapi.models import db_session
from beetsdbwebapi.schema import schema

# Temporary mock data.
ALBUMS = [
    {'id': 1,
     'album': 'Nevermind',
     'albumartist': 'Nirvana',
     'year': 1993,
     'genre': 'Rock'},
    {'id': 2,
     'album': 'Kind Of Blue',
     'albumartist': 'Miles Davis',
     'year': 1959,
     'genre': 'Jazz'},
]

app = Flask(__name__)

app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True
        )
)

# Optional, for adding batch query support (used in Apollo-Client)
# app.add_url_rule(
#         '/graphql/batch',
#         view_func=GraphQLView.as_view(
#             'graphql',
#             schema='{ hello }',
#             batch=True
#         )
# )


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/albums', methods=['GET'])
def get_albums():
    return jsonify({'albums': ALBUMS})


@app.route('/albums/<int:album_id>', methods=['GET'])
def get_album(album_id):
    found_albums = [album for album in ALBUMS if album['id'] == album_id]
    if len(found_albums) == 0:
        abort(404)
    else:
        album = found_albums[0]
    return jsonify({'album': album})


@app.route('/albums', methods=['POST'])
def create_album():
    if not request.json:
        abort(400)

    album = {
        'id': ALBUMS[-1]['id'] + 1,
        'album': request.json['album'],
        'albumartist': request.json['albumartist'],
        'year': request.json['year'],
        'genre': request.json['genre']
    }
    ALBUMS.append(album)
    return jsonify({'album': album}), 201


@app.route('/albums/<int:album_id>', methods=['PUT'])
def update_album(album_id):
    if not request.json:
        abort(400)

    found_albums = [album for album in ALBUMS if album['id'] == album_id]
    if len(found_albums) == 0:
        abort(404)
    else:
        album = found_albums[0]

    album['album'] = request.json.get('album', album['album'])
    album['albumartist'] = request.json.get(
                                    'albumartist',
                                    album['albumartist']
                           )
    album['year'] = request.json.get('year', album['year'])
    album['genre'] = request.json.get('genre', album['genre'])

    return jsonify({'album': album})


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True)
