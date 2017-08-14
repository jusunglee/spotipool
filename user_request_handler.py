import spotify_functions as sf
import database as db

def handle_track_suggestion(user_id, playlist_id, song_id_list):
    db_config = db.haspermissions(user_id, playlist_id)
    if db_config['status'] == 'error':
        return db_config['error']
    username = db_config['username']

    # enum 0: Add songs immediately to playlist
    if db_config['enum'] == '0':
        for song_id in song_id_list:
            sf.add_track_to_playlist(username, song_id, playlist_id)
    return {'status': 'success'}