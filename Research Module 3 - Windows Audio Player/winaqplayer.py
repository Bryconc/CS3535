__author__ = 'Brycon'

import winplayer
import wave
import os
import tempfile

from echonest.remix.support.ffmpeg import ffmpeg

TEMP_DIRECTORY = "Temp_Folder"


class WinAQPlayer(winplayer.WinPlayer):

    def __init__(self, audio):
        super(WinAQPlayer, self).__init__()
        self.audio = audio
        self.wav_file = wave.open(self.get_wav(), 'rb')
        self.temp_files = []
        #WinAQPlayer._clear_temp()

    def add_audio(self, AudioQuantum):
        wav_file = self.wav_file

        name = WinAQPlayer._generate_name()
        temp_file = wave.open(name, 'wb')

        number_of_frames = int(AudioQuantum.duration * wav_file.getframerate())
        start_frame = int(AudioQuantum.start * wav_file.getframerate())

        wav_file.setpos(start_frame)
        temp_file.setnchannels(wav_file.getnchannels())
        temp_file.setsampwidth(wav_file.getsampwidth())
        temp_file.setframerate(wav_file.getframerate())
        temp_file.writeframesraw(wav_file.readframes(number_of_frames))
        temp_file.close()
        super(WinAQPlayer, self).add_audio(name)

        self.temp_files.append(name)

    @staticmethod
    def _generate_name():
        from uuid import uuid4

        while True:
            temp = uuid4().hex + ".wav"
            if not os.path.isfile(TEMP_DIRECTORY + "/" + temp):
                return TEMP_DIRECTORY + "/" + temp

    @staticmethod
    def _clear_temp():
        for f in os.listdir(TEMP_DIRECTORY):
            os.remove(TEMP_DIRECTORY + "/" + f)

    def close(self):
        for f in self.temp_files:
            os.remove(f)

        self.wav_file.close()
        self.audio.unload()

    def get_wav(self):
        if self.audio.filename.lower().endswith(".wav") and (self.audio.sampleRate, self.audio.numChannels) == (44100, 2):
            file_to_read = self.audio.filename
        elif self.audio.convertedfile:
            file_to_read = self.audio.convertedfile
        else:
            temp_file_handle, self.audio.convertedfile = tempfile.mkstemp(".wav")
            self.audio.sampleRate, self.audio.numChannels = ffmpeg(self.self.audio.filename,
                                                                   self.self.audio.convertedfile, overwrite=True,
                                                                   numChannels=self.self.audio.numChannels,
                                                                   sampleRate=self.self.audio.sampleRate, verbose=self.self.audio.verbose)
            file_to_read = self.self.audio.convertedfile
        return file_to_read