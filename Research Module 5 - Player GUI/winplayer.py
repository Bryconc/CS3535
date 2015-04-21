__author__ = 'Brycon'

import Queue as q
import threading
import os
import winsound

import player_gui as gui


class WinPlayer(object):
    def __init__(self, title="Player", spotify=None):
        self.song_queue = q.Queue()
        self.play_thread = PlayThread(self, threading.Event())
        self.playing = False
        self.play_thread.pause()
        self.play_thread.start()
        self.spotify = spotify

        self.player_gui = gui.PlayerGUI(self, title)
        self.player_gui.show()
        self.player_gui.start_timer()

    def add_audio(self, audio, track):
        if not WinPlayer.__is_wav_file(audio):
            raise TypeError("File must be of type .WAV")
        self.song_queue.put((audio, track))

    def play(self):
        if not self.playing:
            self.playing = True
            self.play_thread.play()

    def pause(self):
        if self.playing:
            self.playing = False
            self.play_thread.pause()
            print("Player will pause at the end of the current audio.")

    def update_current_song(self, track):
        self.player_gui.update_track(track)

    def get_next_audio(self):
        return self.song_queue.get()

    @staticmethod
    def __is_wav_file(audio):
        file_name, file_extension = os.path.splitext(audio)
        return file_extension == '.wav'


class PlayThread(threading.Thread):
    def __init__(self, player, event):
        super(PlayThread, self).__init__()
        self.player = player
        self.play_event = event

    def run(self):
        while True:
            if self.play_event.is_set():
                next_audio, track = self.player.get_next_audio()
                print("Playing " + track['track']['name'])
                self.player.update_current_song(track)
                winsound.PlaySound(next_audio, winsound.SND_FILENAME | winsound.SND_NOSTOP)
                os.remove(next_audio)
            else:
                self.play_event.wait()

    def pause(self):
        self.play_event.clear()

    def play(self):
        self.play_event.set()

