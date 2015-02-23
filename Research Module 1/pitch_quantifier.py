__author__ = 'Brycon'

import sys
import numpy as np
import echonest.remix.audio as audio
import matplotlib.pyplot as plot

usage = """
Usage:
    python pitch_quantifier.py [input_filename]+

Example:
    python pitch_quantifier.py Song1.mp3 Song2.mp3

"""

title = "Pitch Frenquency Count for "

pitches = [0] * 12

def add_song_pitches(input_file):
    try:
        audiofile = audio.LocalAudioFile(input_file)
        segments = audiofile.analysis.segments
        for segment in segments.pitches:
            add_to_vector(segment)

    except Exception as e:
        print("File specified not found.")

def add_to_vector(pitch_vect):
    # for i in range(0, 12):
    #     pitches[i] += pitch_vect[i]
    global pitches
    pitches = np.add(pitches, pitch_vect)

def graph_pitches():
    pitch_values = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']

    width = 0.75
    ind = np.arange(12)

    fig, ax = plot.subplots()
    ax.bar(ind, pitches)
    ax.set_xlabel('Pitches')
    ax.set_ylabel('Recurrence Values')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(pitch_values)

    plot.title(title)
    plot.savefig(title + ".png")
    plot.show()

if __name__ == "__main__":
    number_songs = len(sys.argv)
    if number_songs < 2:
        print usage
        sys.exit(-1)
    else:

        for i in range(1, number_songs):
            add_song_pitches(sys.argv[i])
            if number_songs == 2:
                title += sys.argv[i]
            elif i < number_songs - 1:
                title += sys.argv[i] + ", "
            else:
                title += "and " + sys.argv[i]
        graph_pitches()
