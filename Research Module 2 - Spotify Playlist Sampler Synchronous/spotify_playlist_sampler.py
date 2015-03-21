__author__ = 'Brycon'

import spotipy
import spotipy.util as util

import echonest.remix.audio as audio
from echonest.remix.support.ffmpeg import ffmpeg

import sys
import winsound
import tempfile
import random
import urllib

TEST_SIZE = 5
DEBUG_TRACK = True

master_track_list = []
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

        while tracks["next"]:
            tracks = sp.next(tracks)
            add_tracks(tracks)

        add_sampled_tracks()

        print("Obtained %d tracks with previews" % len(track_list))

        print("Playing samples")
        while samples:
            index = random.randint(0, len(track_list) - 1)
            sample = samples[index]
            samples.remove(sample)
            track = track_list[index]
            track_list.remove(track)
            print("Playing %s - %s" % (track["track"]["name"], track["track"]["artists"][0]["name"]))
            winsound.PlaySound(get_wav(sample), winsound.SND_FILENAME)


def add_tracks(tracks):
    for track in tracks["items"]:
        if track['track']['preview_url']:
            master_track_list.append(track)


def add_sampled_tracks():
    for i in range(TEST_SIZE):
        index = random.randint(0, len(master_track_list) - 1)
        track = master_track_list[index]
        master_track_list.remove(track)
        track_list.append(track)
        print("%d. Added %s" % (len(track_list), track['track']['name']))
        print("Downloading %s" % track['track']['preview_url'])
        mp3file, headers = urllib.urlretrieve(track['track']['preview_url'], "test.mp3")
        samples.append(audio.LocalAudioFile(mp3file))


#   Old method of adding tracks that always picked in the same order.
# def add_tracks(tracks):
#     for track in tracks["items"]:
#         if track['track']['preview_url'] and len(track_list) < TEST_SIZE:
#             track_list.append(track)
#             print("%d. Added %s" % (len(track_list), track['track']['name']))
#
#             if DEBUG_TRACK:
#                 from pprint import pprint
#                 pprint(track)
#                 exit()
#
#             print("Downloading %s" % track['track']['preview_url'])
#             mp3file, headers = urllib.urlretrieve(track['track']['preview_url'], "test.mp3")
#             samples.append(audio.LocalAudioFile(mp3file))

def get_wav(audio_file):  # Code modified from Luke Stack's aqplayer.
        """
        Helper method for __init__
        :return .wav file from the LocalAudioFile
        """
        if audio_file.filename.lower().endswith(".wav") and (audio_file.sampleRate, audio_file.numChannels) == (44100, 2):
            file_to_read = audio_file.filename
        elif audio_file.convertedfile:
            file_to_read = audio_file.convertedfile
        else:
            temp_file_handle, audio_file.convertedfile = tempfile.mkstemp(".wav")
            audio_file.af.sampleRate, audio_file.numChannels = ffmpeg(audio_file.filename, audio_file.convertedfile, overwrite=True,
                    numChannels=audio_file.numChannels, sampleRate=audio_file.sampleRate, verbose=audio_file.verbose)
            file_to_read = audio_file.convertedfile
        return file_to_read


if __name__ == "__main__":
    if len(sys.argv) > 2:
        sample_playlist(sys.argv[1], sys.argv[2])
    else:
        print "ERROR - Need a user and a playlist ID!"
        print "usage: python spotify_playlist_sampler.py [user] [playlistID]"
        print "example: python spotify_playlist_sampler.py george_spv 6nhiBJot8yHf2BHoRrBUmJ"