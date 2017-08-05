from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import spotify_functions as sf
import database as db

app = Flask(__name__)


@app.route('/')
def index():
    user = {
        'name': 'jusung',
        'company': 'microsoft'}
    title = "jusung's world"
    data = {
        'title': title,
        'user': user
    }
    return render_template('index.html', data=data)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/playlist/', methods=['POST'])
def post_create_playlist():
    spotify_user_id = request.form['user_id']
    playlist_name = request.form['playlist_name']
    # status = create_playlist(spotify_user_id, playlist_name)
    # return jsonify(status)
    return


@app.route('/playlist/song', methods=['POST'])
def post_add_track_to_playlist():
    spotify_user_id = request.form['user_id']
    playlist_id = request.form['playlist_id']
    track_id = request.form['track_id']
    search_result = sf.add_track_to_playlist(spotify_user_id, playlist_id, track_id)
    return jsonify(search_result)


@app.route('/track/')
@app.route('/track/<string_query>')
def get_search_track(string_query=None):
    sp = sf.load_spotipy_object(sf.load_keys())
    return jsonify(sf.get_tracks_from_string_query(sp, string_query))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
