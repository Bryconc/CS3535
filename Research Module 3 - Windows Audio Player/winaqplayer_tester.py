__author__ = 'Brycon'

import os

import echonest.remix.audio as audio

import winaqplayer as wp


def main():
    test_directory = "Test_MP3_Files"

    files = [f for f in os.listdir(test_directory) if os.path.isfile(os.path.join(test_directory, f))]

    audio_file = audio.LocalAudioFile("%s/%s" % (test_directory, files[0]))
    bars = audio_file.analysis.bars
    # shuffle(bars)

    print("Initalizing player...")
    player = wp.WinAQPlayer(audio_file)

    player.play()
    for bar in bars:
        player.add_audio(bar)
        print("Adding new bar")


if __name__ == "__main__":
    main()