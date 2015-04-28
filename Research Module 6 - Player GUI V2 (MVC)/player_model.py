__author__ = 'Brycon'

import subprocess as sp
from functools import partial
from random import shuffle

import spotipy
import spotipy.util

import winplayer
from util.threads import DownloaderThread, AnalyzerThread
from util.observable import Observable

CLIENT_ID = "1e9958fdd24746aea8959ccf6f724441"
CLIENT_SECRET = "a5bcdc07002c463f87a7d827c1638b91"
REDIRECT_URI = "http://student.cs.appstate.edu/carpenterba/SpotifySampler/callback.html"


class Model(Observable):
    def __init__(self):
        super(Model, self).__init__()

        self.master_track_list = []
        self.playlist_list = []
        self.favorites_list = []
        self.current_track_number = 0
        self.playlist_amount = 0

        self.current_track = None
        self.player = None
        self.analyzer = None
        self.downloader = None

    def setup(self):
        if not self.spotify_playlist:
            raise InvalidInputException("You must set the spotify playlist, before you can start the player.")

        if self.player:
            call_play = True
        else:
            call_play = False

        print("\nSampling playlist: %s" % self.spotify_playlist["name"])
        self.__load_tracks()
        self.playlist_amount = self.get_playlist_track_number()
        print("With a total of %d preview-able tracks" % self.playlist_amount)
        self.current_track_number = 0

        self.player = winplayer.WinPlayer(self.notify_observers)
        self.analyzer = AnalyzerThread(self.player, self.playlist_amount)
        self.analyzer.start()
        self.downloader = DownloaderThread(self.analyzer, self.playlist_amount)
        self.downloader.start()

        if call_play:
            self.on()

        self.__grab_tracks()

    def on(self):
        self.player.play()

    def off(self):
        self.player.pause()

    def set_spotify_playlist(self, username, playlist):
        self.__set_spotipy_info(username, playlist)
        token = self.__request_spotipy_token()
        if token:
            self.__request_spotipy_object(token)
            self.__retrieve_playlist()
        self.setup()

    def get_current_track(self):
        return self.current_track

    def get_current_track_number(self):
        return self.current_track_number

    def get_playlist_amount(self):
        return self.playlist_amount

    def get_favorites_list(self):
        return self.favorites_list

    def get_master_track_list(self):
        return self.master_track_list

    def get_playlist_list(self):
        return self.playlist_list

    def get_playlist(self):
        return self.spotify_playlist

    def get_playlist_track_number(self):
        return len(self.master_track_list)

    def shuffle_playlist(self):
        shuffle(self.master_track_list)

    def notify_observers(self, *args, **kwargs):
        if 'track' in kwargs:
            self.current_track = kwargs['track']
            self.current_track_number += 1

        super(Model, self).notify_observers(*args, **kwargs)

    def unload_player(self, callback, wait=True):
        if self.player:
            self.player.stop()
            if self.player.paused():
                wait = False
            if self.player.get_time() > 30:
                wait = False

        if self.analyzer:
            self.analyzer.stop()
            self.analyzer.unload()

        if self.downloader:
            self.downloader.stop()
            DownloaderThread.unload()

        if self.player and wait:
            self.player.wait_until_finished(callback)

    def new_playlist(self, user_id, playlist_id):
        if self.player:
            self.unload_player(partial(self.set_spotify_playlist, user_id, playlist_id))
        else:
            self.set_spotify_playlist(user_id, playlist_id)

    def export_favorites(self, export_type, **kwargs):
        print("Exporting favorites type %s" % export_type)
        if export_type == 'csv':
            self.export_csv(**kwargs)
        elif export_type == 'existing':
            print("In here")
            self.export_existing_playlist(kwargs["user"], kwargs["playlist"])

    def export_csv(self, **kwargs):
        file_name = kwargs['file_name']
        information = kwargs['information']

        with open(file_name + ".csv", 'w') as csv_file:
            for track in self.favorites_list:
                information_list = []

                if 'name' in information:
                    information_list.append(track['track']['name'])

                if 'artists' in information:
                    artists = [x['name'] for x in track['track']['artists']]
                    information_list.append("-".join(artists))

                if 'album' in information:
                    information_list.append(track['track']['album']['name'])

                if 'preview_url' in information:
                    information_list.append(track['track']['preview_url'])

                csv_file.write(",".join(information_list) + "\n")

        sp.call(["notepad.exe ", file_name + ".csv"])

    def export_existing_playlist(self, user, playlist):
        self.__append_to_playlist(user, playlist)

    ###################################
    # #
    # BEGIN PRIVATE UTILITY METHODS  #
    #                                 #
    ###################################

    def __set_spotipy_info(self, username, playlist_id):
        self.spotipy_username = username
        self.spotipy_playlist_id = playlist_id

    def __request_spotipy_token(self):
        if not self.spotipy_username or not self.spotipy_playlist_id:
            raise InvalidInputException("You must set the spotipy information first.")

        scopes = 'playlist-modify-public playlist-modify-private'

        return spotipy.util.prompt_for_user_token(self.spotipy_username, scope=scopes, client_id=CLIENT_ID,
                                                  client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)

    def __request_spotipy_object(self, token):
        if not token:
            raise InvalidInputException("You must request a valid authentication token first")
        self.sp = spotipy.Spotify(auth=token)

    def __retrieve_playlist(self):
        if not self.spotipy_username or not self.spotipy_playlist_id:
            raise InvalidInputException("You must set the spotipy information first.")

        if not self.sp:
            raise InvalidInputException("You must request a Spotipy object first.")
        self.spotify_playlist = self.sp.user_playlist(self.spotipy_username, self.spotipy_playlist_id)

    def __load_tracks(self):
        tracks = self.spotify_playlist["tracks"]

        self.__add_tracks(tracks)

        while tracks['next']:
            tracks = self.sp.next(tracks)
            self.__add_tracks(tracks)

        self.shuffle_playlist()
        self.notify_observers(load=True)

    def __add_tracks(self, track_list):
        for track in track_list["items"]:
            if track['track']['preview_url']:
                self.master_track_list.append(SpotifyTrack(track))

    def __grab_tracks(self):
        for i in range(self.get_playlist_track_number()):
            track = self.master_track_list[0]
            self.master_track_list.remove(track)
            self.downloader.queue_download(track)

    def __append_to_playlist(self, user, playlist):
        track_ids = self.__get_favorites_track_ids()
        self.sp.user_playlist_add_tracks(user, playlist, track_ids)

    def __get_favorites_track_ids(self):
        result = []
        for track in self.favorites_list:
            result.append(track['track']['id'])
        return result


class InvalidInputException(Exception):
    def __init__(self, message):
        super(InvalidInputException, self).__init__(message)


class SpotifyTrack(dict):
    def __init__(self, *args, **kwargs):
        super(SpotifyTrack, self).__init__(*args, **kwargs)

    def __str__(self):
        if 'track' in self:
            try:
                return self.get('track').get('name')
            except UnicodeEncodeError:
                return self.get('track').get('name').encode('utf-8')

        return super(SpotifyTrack, self).__str__()





