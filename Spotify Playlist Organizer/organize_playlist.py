__author__ = 'Brycon'

import spotipy
from spotipy.util import prompt_for_user_token

KEY = 'ALBUM'
DESCENDING_ORDER = False
PLAYLIST_URL = 'https://play.spotify.com/user/bryconc/playlist/4yumoVCxw7K4roD5POtqCP'
SPOTIFY_USERNAME = 'bryconc'

CLIENT_ID = '851f899cc4664f7cbf6491fe89ac98c5'
CLIENT_SECRET = '5b1fcdb9f7e14b77b3258a8020cfd48b'
REDIRECT_URI = 'http://student.cs.appstate.edu/carpenterba/SpotifySampler/callback.html'


def main():
    user_id, playlist_id = parse_spotify_playlist_url(PLAYLIST_URL)
    scopes = 'playlist-modify-public playlist-modify-private playlist-read-private'
    token = prompt_for_user_token(SPOTIFY_USERNAME, scopes, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                  redirect_uri=REDIRECT_URI)
    if token:
        sp = spotipy.Spotify(token)
        playlist = sp.user_playlist(user_id, playlist_id)
        tracklist = tracklist_from_playlist(sp, playlist['tracks'])
        print("Organizing playlist " + playlist['name'] + " by " + KEY.lower())
        sorted_tracklist = sorted(tracklist, key=get_key(), reverse=DESCENDING_ORDER)
        track_ids = track_ids_from_tracklist(sorted_tracklist)
        for tracks in track_ids:
            sp.user_playlist_remove_all_occurrences_of_tracks(user_id, playlist_id, tracks)
            sp.user_playlist_add_tracks(user_id, playlist_id, tracks)

    else:
        print("Authentication failed.")


def parse_spotify_playlist_url(url):
    import re

    regex = r'./user/(?P<user_id>[a-zA-z0-9]+)/playlist/(?P<playlist_id>[a-zA-z0-9]+)'
    regexp = re.compile(regex)
    result = regexp.search(url)
    return result.group('user_id'), result.group('playlist_id')


def tracklist_from_playlist(sp, playlist):
    track_list = []
    for track in playlist["items"]:
        track_list.append(track)

    while playlist["next"]:
        playlist = sp.next(playlist)
        for track in playlist["items"]:
            track_list.append(track)

    return track_list


def track_ids_from_tracklist(tracklist):
    track_ids = []
    current_list = []
    for i, track in enumerate(tracklist):
        current_list.append(track['track']['id'])
        if (i % 99 == 0 and i > 0) or i == len(tracklist) - 1:
            track_ids.append(current_list)
            current_list = []

    return track_ids


def get_key():
    if KEY == 'ALBUM':
        return lambda k: k['track']['album']['name']
    if KEY == 'ARTIST':
        return lambda k: combined_artist_name(k['track']['artists'])
    if KEY == 'TRACK_NAME':
        return lambda k: k['track']['name']


def combined_artist_name(artists):
    artist_names = []
    for artist in artists:
        artist_names.append(artist['name'])

    return " ".join(artist_names)


if __name__ == "__main__":
    main()