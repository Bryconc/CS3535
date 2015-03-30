__author__ = 'Brycon'

import os
import winaqplayer as wp

import echonest.remix.audio as audio

def main():
    test_directory = "Test_MP3_Files"

    files = [f for f in os.listdir(test_directory) if os.path.isfile(os.path.join(test_directory, f))]

    audio_file = audio.LocalAudioFile("%s/%s" % (test_directory, f))
    bars = audio_file.analysis.bars
    from random import shuffle
    shuffle(bars)

    player = wp.WinAQPlayer(audio_file)

    player.play()

    for bar in bars:
        player.add_audio(bar)





if __name__ == "__main__":
    main()