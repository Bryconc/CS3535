__author__ = 'Brycon'

import sys
import os
import tempfile
import random
import urllib
import threading
import Queue as q

import spotipy
import spotipy.util as util
import echonest.remix.audio as audio
from echonest.remix.support.ffmpeg import ffmpeg

import winplayer as wp


DEBUG_ANALYZER = True

master_track_list = []
track_list = []
samples = []


def sample_playlist(user, playlist_id):
    token = util.prompt_for_user_token(user, client_id="1e9958fdd24746aea8959ccf6f724441",
                                       client_secret="a5bcdc07002c463f87a7d827c1638b91",
                                       redirect_uri="http://www.google.com")
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

        print("Setting up...")
        m, s = divmod(len(master_track_list) * 30, 60)
        h, m = divmod(m, 60)
        time = "%d:%02d:%02d" % (h, m, s)
        print("Approximate playtime: " + time)

        amount = len(master_track_list)
        player = wp.WinPlayer()
        analyzer = AnalyzerThread(player, amount)
        downloader = DownloaderThread(analyzer, amount)

        downloader.start()
        analyzer.start()

        player.play()

        for i in range(len(master_track_list)):
            index = random.randint(0, len(master_track_list) - 1)
            track = master_track_list[index]
            master_track_list.remove(track)
            track_list.append(track)
            downloader.queue_download(track)


def add_tracks(tracks):
    for track in tracks["items"]:
        if track['track']['preview_url']:
            master_track_list.append(track)


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
        audio_file.af.sampleRate, audio_file.numChannels = ffmpeg(audio_file.filename, audio_file.convertedfile,
                                                                  overwrite=True,
                                                                  numChannels=audio_file.numChannels,
                                                                  sampleRate=audio_file.sampleRate,
                                                                  verbose=audio_file.verbose)
        file_to_read = audio_file.convertedfile
    return file_to_read


class DownloaderThread(threading.Thread):
    def __init__(self, analyzer_thread, amount=0):
        super(DownloaderThread, self).__init__()
        self.download_queue = q.Queue()
        self.analyzer_thread = analyzer_thread
        self.amount = amount
        self.downloaded = 0

    def queue_download(self, track):
        self.download_queue.put(track)

    def run(self):
        while self.downloaded < self.amount:
            track = self.download_queue.get()
            # print("Downloading " + file.get_name() + ": File %d of %d" % (self.downloaded, self.amount))
            if not os.path.isfile("Temp_Directory/" + track['track']['id'] + ".mp3"):
                mp3file, headers = urllib.urlretrieve(track['track']['preview_url'],
                                                      "Temp_Directory/" + track['track']['id'] + ".mp3")
                self.analyzer_thread.queue_analysis(mp3file, track)
            else:
                self.analyzer_thread.queue_analysis("Temp_Directory/" + track['track']['id'] + ".mp3", track)
            self.downloaded += 1
        print("Downloader closing.")


class AnalyzerThread(threading.Thread):
    def __init__(self, player, amount=0):
        super(AnalyzerThread, self).__init__()
        self.analyze_queue = q.Queue()
        self.player = player
        self.amount = amount
        self.analyzed = 0

    def queue_analysis(self, file, track):
        self.analyze_queue.put((file, track))

    def run(self):
        while self.analyzed < self.amount:
            try:
                mp3file, track = self.analyze_queue.get()
                verbose = DEBUG_ANALYZER
                # print("Processing " + track['track']['name'] + ". %d left on queue." % self.analyze_queue.qsize())
                af = audio.LocalAudioFile(mp3file, verbose=verbose)
                wav = get_wav(af)
                if self.analyzed == 0:
                    print("Setup complete!")
                self.player.add_audio(wav, track['track']['name'])
                os.remove(mp3file)
                self.analyzed += 1
            except Exception as e:
                print("***** Error processing " + track['track']['name'] + " *****")
                from pprint import pprint

                pprint(track['track'])
                print(e)
                self.amount -= 1

        print("Analyzer closing!")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        sample_playlist(sys.argv[1], sys.argv[2])
    else:
        print "ERROR - Need a user and a playlist ID!"
        print "usage: python spotify_playlist_sampler_pydub.py [user] [playlistID]"
        print "example: python spotify_playlist_sampler_pydub.py george_spv 6nhiBJot8yHf2BHoRrBUmJ"