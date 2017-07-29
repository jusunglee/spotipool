from spotify_functions import *


def run_all_tests():
    sp = load_spotipy_object(load_keys())
    test_search(sp)


def test_search(sp):
    """Tests the spotipy search function for a song using string query

    Args:
        sp: preconfigured spotipy.Spotify() object

    Returns:
        items: list of json object in the following format:
        {'song_id': '296mmTJOJ904FwHQsSBdDr',
        'song_name': 'Champagne & Sunshine',
        'artist_name': 'PLVTINUM',
        'artist_id': '4V2pR2iSd1g0RZCglrP3jn',
        'song_uri': 'spotify:track:296mmTJOJ904FwHQsSBdDr'}
    """
    items = get_tracks_from_string_query(sp, 'Champagne and Sunshine')
    for item in items:
        print(item,'\n')
    return items


run_all_tests()
