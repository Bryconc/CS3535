# By Brycon Carpenter
# Based on the Cowbell example from remix-examples by Rob Ochshorn and Adam Baratz.
# Modified to insert hard base instead of cowbell

import numpy
import os
import random
import time

import echonest.remix.audio as audio

usage = """
Usage: 
    python hardbase.py <inputFilename> <outputFilename> <baseIntensity>

Example:
    python hardbase.py YouCanCallMeAl.mp3 YouCanCallMeBase.mp3 0.2

Reference:
    http://www.youtube.com/watch?v=ZhSkRHXTKlw
"""


# constants
BASE_THRESHOLD = 0.85
BASE_OFFSET = -0.005

# samples
soundsPath = "sounds/"

baseSounds = map(lambda x: audio.AudioData(os.path.join(soundsPath, "base%s.wav" % x), sampleRate=44100, numChannels=2), range(10))
trill = audio.AudioData(os.path.join(soundsPath, "trill.wav"), sampleRate=44100, numChannels=2)

def linear(input, in1, in2, out1, out2):
    return ((input-in1) / (in2-in1)) * (out2-out1) + out1

def exp(input, in1, in2, out1, out2, coeff):
    if (input <= in1):
        return out1
    if (input >= in2):
        return out2
    return pow( ((input-in1) / (in2-in1)) , coeff ) * (out2-out1) + out1

class Base:
    def __init__(self, input_file):
        self.audiofile = audio.LocalAudioFile(input_file)
        self.audiofile.data *= linear(self.audiofile.analysis.loudness, -2, -12, 0.5, 1.5) * 0.75

    def run(self, BASE_intensity, out):
        if BASE_intensity != -1:
            self.BASE_intensity = BASE_intensity
        t1 = time.time()
        sequence = self.sequence(baseSounds)
        print "Sequence and mixed in %g seconds" % (time.time() - t1)
        self.audiofile.encode(out)

    def sequence(self, chops):
        # add bases on the beats
        for beat in self.audiofile.analysis.beats:
            volume = linear(self.BASE_intensity, 0, 1, 0.1, 0.3)
            # mix in base on beat
            if self.BASE_intensity == 1:
                self.mix(beat.start+BASE_OFFSET, seg=baseSounds[random.randint(0,1)], volume=volume)
            else:
                self.mix(beat.start+BASE_OFFSET, seg=baseSounds[random.randint(2,4)], volume=volume)
            # divide beat into quarters
            quarters = (numpy.arange(1,4) * beat.duration) / 4. + beat.start
            # mix in base on quarters
            for quarter in quarters:
                volume = exp(random.random(), 0.5, 0.1, 0, self.BASE_intensity, 0.8) * 0.3
                pan = linear(random.random(), 0, 1, -self.BASE_intensity, self.BASE_intensity)
                if self.BASE_intensity < BASE_THRESHOLD:
                    self.mix(quarter+BASE_OFFSET, seg=baseSounds[2], volume=volume)
                else:
                    randomBase = linear(random.random(), 0, 1, BASE_THRESHOLD, 1)
                    if randomBase < self.BASE_intensity:
                        self.mix(start=quarter+BASE_OFFSET, seg=baseSounds[random.randint(0,1)], volume=volume)
                    else:
                        self.mix(start=quarter+BASE_OFFSET, seg=baseSounds[random.randint(2,4)], volume=volume)
        for section in self.audiofile.analysis.sections[1:]:
            sample = trill
            volume = 0.3
            self.mix(start=section.start+BASE_OFFSET, seg=sample, volume=volume)

    def mix(self, start=None, seg=None, volume=0.3, pan=0.):
        # this assumes that the audios have the same frequency/numchannels
        startsample = int(start * self.audiofile.sampleRate)
        seg = seg[0:]
        seg.data *= (volume-(pan*volume), volume+(pan*volume)) # pan + volume
        if self.audiofile.data.shape[0] - startsample > seg.data.shape[0]:
            self.audiofile.data[startsample:startsample+len(seg.data)] += seg.data[0:]


def main(inputFilename, outputFilename, baseIntensity) :
    c = Base(inputFilename)
    print 'baseing...'
    c.run(baseIntensity,  outputFilename)

if __name__ == '__main__':
    import sys
    try :
        inputFilename = sys.argv[1]
        outputFilename = sys.argv[2]
        baseIntensity = float(sys.argv[3])
    except :
        print usage
        sys.exit(-1)
    main(inputFilename, outputFilename, baseIntensity)
