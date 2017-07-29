import spotipy
import spotipy.util as util
import os
from json.decoder import JSONDecodeError

# Prepare tokens and authorization
client_id = ''
client_secret = ''
playlist_id = ''
username = ''
redirect_uri = 'http://localhost/'
keys = 'keys.txt'

with open(keys) as file_:
    content = file_.readlines()

for line in content:
    tokens = line.split('=')
    tokens = [token.strip() for token in tokens]
    if tokens[0] == 'client_id':
        client_id = tokens[1]
    elif tokens[0] == 'client_secret':
        client_secret = tokens[1]
    elif tokens[0] == 'username':
        username = tokens[1]
    elif tokens[0] == 'playlist_id':
        playlist_id = tokens[1]
    else:
        print('Unknown header from keys file.')

scope = 'playlist-modify-public'
user_token = ''
sp = None

try:
    user_token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    user_token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

if user_token:
    sp = spotipy.Spotify(auth=user_token)
    sp.trace = False


def get_tracks_from_string_query(string_query):
    results = sp.search(string_query)['tracks']['items']
    return_list = []
    for result in results:
        return_list.append({
            'song_id': result['id'],
            'song_name': result['name'],
            'artist_name': result['album']['artists'][0]['name'],
            'artist_id': result['album']['artists'][0]['id'],
            'song_uri': result['uri']
        })
    return return_list


def test_search():
    items = get_tracks_from_string_query('Migos')
    for item in items:
        print(item,'\n')
    return items




print(test_search())