__author__ = 'Brycon'

import os
import Queue
import ssl
import tempfile
import threading
import urllib

import echonest.remix.audio as audio
import echonest.remix.support.ffmpeg as ffmpeg


DEBUG_ANALYZER = False

DOWNLOAD_DIRECTORY = "util/Temp_Directory/"


class DownloaderThread(threading.Thread):
    def __init__(self, analyzer_thread, amount=0):
        super(DownloaderThread, self).__init__()
        self.download_queue = Queue.Queue()
        self.analyzer_thread = analyzer_thread
        self.amount = amount
        self.downloaded = 0
        self.running = False

    def queue_download(self, track):
        self.download_queue.put(track)

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        while self.downloaded < self.amount and self.running:
            try:
                track = self.download_queue.get()
                if not os.path.isfile(DOWNLOAD_DIRECTORY + track['track']['id'] + ".mp3"):
                    mp3file, headers = urllib.urlretrieve(track['track']['preview_url'],
                                                          DOWNLOAD_DIRECTORY + track['track']['id'] + ".mp3")
                    self.analyzer_thread.queue_analysis(mp3file, track)
                else:
                    self.analyzer_thread.queue_analysis(DOWNLOAD_DIRECTORY + track['track']['id'] + ".mp3", track)
                self.downloaded += 1
            except ssl.SSLError:
                self.queue_download(track)

    @staticmethod
    def unload():
        for dl_file in os.listdir(DOWNLOAD_DIRECTORY):
            if dl_file.endswith(".mp3"):
                try:
                    os.remove(DOWNLOAD_DIRECTORY + dl_file)
                except WindowsError:
                    print("Error with " + dl_file)


class AnalyzerThread(threading.Thread):
    def __init__(self, player, amount=0):
        super(AnalyzerThread, self).__init__()
        self.analyze_queue = Queue.Queue()
        self.player = player
        self.amount = amount
        self.analyzed = 0
        self.running = False
        self.af_list = []

    def stop(self):
        self.running = False

    def queue_analysis(self, mp3_file, track):
        self.analyze_queue.put((mp3_file, track))

    def run(self):
        self.running = True
        while self.analyzed < self.amount and self.running:
            try:
                mp3file, track = self.analyze_queue.get()
                af = audio.LocalAudioFile(mp3file, verbose=DEBUG_ANALYZER)
                self.af_list.append(af)
                wav = AnalyzerThread.__get_wav(af)
                self.player.add_audio(wav, track)
                os.remove(mp3file)
                self.analyzed += 1
            except Exception as e:
                print("***** Error processing " + track['track']['name'] + " *****")
                self.amount -= 1

    def unload(self):
        print("Deleting temp wav files")
        for af in self.af_list:
            try:
                af.unload()
            except WindowsError:
                print("Error with " + str(af))

    @staticmethod
    def __get_wav(audio_file):  # Code modified from Luke Stack's aqplayer.
        """
        Helper method for __init__
        :return .wav file from the LocalAudioFile
        """
        if audio_file.filename.lower().endswith(".wav") and (audio_file.sampleRate, audio_file.numChannels) == (
        44100, 2):
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