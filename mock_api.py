# Mock lyrics API for testing
# Run API with:
#   flask --app mock_api.py run --debug --port 5001
# Then add API URL to .env:
#   API_URL="http://localhost:5001/{title}/{artist}/"

SONGS = {
    'song 1': {
        'title': 'Song 1',
        'artist': 'Artist A',
        'lyrics': 'These are the lyrics\nto song 1\nby artist A',
    },
    'song 2': {
        'title': 'Song 2',
        'artist': 'Artist A',
        'lyrics': 'These are the lyrics\nto song 2\nby artist A',
    },
    'song 3': {
        'title': 'Song 3',
        'artist': 'Artist B',
        'lyrics': 'These are the lyrics\nto song 3\nby artist B',
    },
}

from flask import Flask
app = Flask(__name__)

@app.get('/<string:title>/')
@app.get('/<string:title>/<string:artist>/')
def api(title, artist=None):
    if title.lower() in SONGS:
        return SONGS[title.lower()]
    else:
        return {}
