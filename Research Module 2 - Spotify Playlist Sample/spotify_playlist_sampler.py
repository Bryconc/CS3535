__author__ = 'Brycon'

import sys
import spotipy
import spotipy.util as util

import echonest.remix.audio as audio

from aqplayer import Player

import random
import urllib

TEST_SIZE = 5

track_list = []
samples = []

def sample_playlist(user, playlist_id):
    token = util.prompt_for_user_token(user, client_id="1e9958fdd24746aea8959ccf6f724441", client_secret="a5bcdc07002c463f87a7d827c1638b91", redirect_uri="http://www.google.com")
    if token:
        sp = spotipy.Spotify(auth=token)
        playlist = sp.user_playlist(user, playlist_id)
        print("\nSampling playlist: %s" % playlist["name"])
        print("With a total of %d tracks" % playlist["tracks"]["total"])

        tracks = playlist["tracks"]

        add_tracks(tracks)

        while tracks["next"] and len(track_list) < TEST_SIZE:
            tracks = sp.next(tracks)
            add_tracks(tracks)


        print("Obtained %d tracks with previews" % len(track_list))

        print("Playing samples")
        while samples:
            sample = random.choice(samples)
            bars = sample.analysis.bars
            aqplayer = Player(sample)
            samples.remove(sample)

            for bar in bars:
                aqplayer.play(bar)

def add_tracks(tracks):
    for track in tracks["items"]:
        if track['track']['preview_url']:
            track_list.append(track)
            print("Added %s" % track['track']['name'])

            print("Downloading %s" % track['track']['preview_url'])
            mp3file, headers = urllib.urlretrieve(track['track']['preview_url'], "test.mp3")
            samples.append(audio.LocalAudioFile(mp3file))








if __name__ == "__main__":
    if len(sys.argv) > 2:
        sample_playlist(sys.argv[1], sys.argv[2])
    else:
        print "ERROR - Need a user and a playlist ID!"
        print "usage: python spotify_playlist_sampler.py [user] [playlistID]"
        print "example: python spotify_playlist_sampler.py george_spv 6nhiBJot8yHf2BHoRrBUmJ"