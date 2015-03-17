__author__ = 'Brycon'

import sys
import spotipy
import spotipy.util as util

def samplePlaylist(user, playlist_id):
    token = util.prompt_for_user_token(user, client_id="1e9958fdd24746aea8959ccf6f724441", client_secret="a5bcdc07002c463f87a7d827c1638b91", redirect_uri="http://www.google.com")
    if token:
        sp = spotipy.Spotify(auth=token)
        playlist = sp.user_playlist(user, playlist_id)
        print("\nSampling playlist: %s" % playlist["name"])
        print("With a total of %d tracks" % playlist["tracks"]["total"])

        tracks = playlist["tracks"]

        show_tracks(tracks)

        while tracks["next"]:
            tracks = sp.next(tracks);
            show_tracks(tracks)

def show_tracks(tracks):
    for i, item in enumerate(tracks["items"]):
        track = item["track"]
        print " %d %32.32s %s" % (i, track["artists"][0]["name"],track["name"])



if __name__ == "__main__":
    if len(sys.argv) > 2:
        samplePlaylist(sys.argv[1], sys.argv[2])
    else:
        print "ERROR - Need a user and a playlist ID!"
        print "usage: python spotify_playlist_sampler.py [user] [playlistID]"
        print "example: python spotify_playlist_sampler.py george_spv 6nhiBJot8yHf2BHoRrBUmJ"