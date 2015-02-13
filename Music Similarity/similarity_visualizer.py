__author__ = 'Brycon'

import sys
import math
import echonest.remix.audio as audio
import matplotlib.pyplot as plot

usage = """
Usage:
    python similarity_visualizer.py <input_filename> <type>

Example:
    python similarity_visualizer.py EverythingIsOnTheOne.mp3 pitch
"""

def main(input_filename, type):
    audiofile = audio.LocalAudioFile(input_filename)
    segments = audiofile.analysis.segments
    similarity_type = "Timbre" if type == "timbre" else "Pitch"
    print("Number of segments : %d" % len(segments))
    timbres = audiofile.analysis.segments.timbre if type == 'timbre' else audiofile.analysis.segments.pitches
    distance_vect = []
    for vect in timbres:
        distance = []
        for vect2 in timbres:
            distance.append(euclidean_distance(vect, vect2));
        distance_vect.append(distance)
    print("Showing plot")
    plot.imshow(distance_vect, cmap="hot")
    plot.title("%s Similarity for %s" % (similarity_type, input_filename))
    plot.colorbar()
    plot.ylabel("Segments")
    plot.xlabel("Segments'")
    plot.savefig(input_filename[:input_filename.rfind('.')] + "_" + similarity_type + ".png")
    plot.show()

def euclidean_distance(vect1, vect2):
    sum_vect = 0
    for i in range(len(vect1)):
        sum_vect += (vect1[i] - vect2[i]) ** 2
    return math.sqrt(sum_vect)


if __name__ == '__main__':
    try:
        input_filename = sys.argv[1]
        type = sys.argv[2]
    except:
        print usage
        sys.exit(-1)
    main(input_filename, type)