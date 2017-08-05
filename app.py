from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from spotify_functions import *


app = Flask(__name__)


@app.route('/')
def index():
    user = {
        'name': 'jusung',
        'company': 'microsoft'}
    title = "jusung's world"
    data = {
        'title': title,
        'user': user}
    return render_template('index.html', data=data)


@app.route('/playlist/', methods=['POST'])
def post_create_playlist():
    spotify_user_id = request.form['user_id']
    playlist_name = request.form['playlist_name']
    status = create_playlist(spotify_user_id, playlist_name)
    return jsonify(status)


@app.route('/playlist/song', methods=['POST'])
def post_add_track_to_playlist():
    spotify_user_id = request.form['user_id']
    playlist_id = request.form['playlist_id']
    track_id = request.form['track_id']
    status = add_track_to_playlist(spotify_user_id, playlist_id, track_id)
    return jsonify(status)


@app.route('/track/')
@app.route('/track/<string_query>')
def get_search_track(string_query=None):
    return jsonify(get_tracks_from_string_query(string_query))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

    
