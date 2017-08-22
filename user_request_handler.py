import spotify_functions as sf
import database as db

def handle_track_suggestion(username, playlist_id, song_id_list):
    for song_id in song_id_list:
        sf.add_track_to_playlist(username, song_id, playlist_id)
    return {'status': 'success'}