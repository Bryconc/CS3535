__author__ = 'Brycon'

import Queue as q
import threading
import os
import winsound


class WinPlayer(object):
    def __init__(self, callback=None):
        self.song_queue = q.Queue()
        self.play_thread = PlayThread(self, threading.Event(), callback)
        self.playing = False
        self.play_thread.pause()
        self.play_thread.start()

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

    def paused(self):
        return self.play_thread.is_paused()

    def stop(self, count=True):
        self.play_thread.stop(count)

    def get_current_song(self):
        return self.play_thread.get_current_song()

    def get_next_audio(self):
        return self.song_queue.get()

    def wait_until_finished(self, callback):
        self.play_thread.call_when_finished(callback)

    def get_time(self):
        return self.play_thread.get_time()


    @staticmethod
    def __is_wav_file(audio):
        file_name, file_extension = os.path.splitext(audio)
        return file_extension == '.wav'


class PlayThread(threading.Thread):
    def __init__(self, player, event, callback):
        super(PlayThread, self).__init__()
        self.player = player
        self.play_event = event
        self.current_audio = None
        self.callback = callback
        self.finish_callback = None
        self.running = False
        self.paused = True
        self.timer = TimerThread(callback)
        self.timer.start()

    def run(self):
        self.running = True
        while True and self.running:
            if self.play_event.is_set():
                self.paused = False
                next_audio, track = self.player.get_next_audio()
                if self.callback:
                    self.callback(track=track)
                self.timer.reset_count()
                winsound.PlaySound(next_audio, winsound.SND_FILENAME | winsound.SND_NOSTOP)
            else:
                self.paused = True
                self.play_event.wait()
        if self.finish_callback:
            self.timer.stop()
            self.finish_callback()

    def stop(self, count):
        self.running = False
        if not count:
            self.timer.stop()

    def get_current_audio(self):
        return self.current_audio

    def pause(self):
        self.play_event.clear()

    def is_paused(self):
        return self.paused

    def play(self):
        self.play_event.set()

    def get_time(self):
        return self.timer.get_count()

    def call_when_finished(self, callback):
        self.finish_callback = callback


class TimerThread(threading.Thread):
    def __init__(self, callback):
        super(TimerThread, self).__init__()
        self.time_event = threading.Event()
        self.count = 0
        self.callback = callback
        self.running = False

    def run(self):
        self.running = True
        while not self.time_event.wait(1) and self.running:
            self.count += 1
            self.callback(count=self.count)

    def stop(self):
        self.running = False

    def get_count(self):
        return self.count

    def reset_count(self):
        self.count = 0
        self.callback(count=self.count)

    def get_count(self):
        return self.count

