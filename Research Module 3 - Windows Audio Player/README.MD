## Windows Queued Asynchronous Player##

The application simulates an asynchronous audio player for the Windows platform. The Player can queue up a line of .WAV files to be played. It also includes an alternative for the aqplayer that does not function well on Windows

**Process**

Once a player is created, you can add .WAV audio files to its internal queue to be played. The player can be paused.

**Dependencies**

The WinPlayer has no outside dependencies. All modules used are native to Python 2.7.9

The WinAQPlayer, however, uses echonest.remix's ffmpeg

**Future Use**

The design was intended to be a module used in future applications that require sound on a Window's platform. The player will be used in my Playlist Sampler Project

**Example**

After importing winplayer you can simply create an instance of the player like so:

```python

    import winplayer as wp

    player = wp.WinPlayer()
```

From there you can begin queueing up audio to be played.

```python

    player.add_audio("test_file.wav")
```

Then you simply tell the player to start playing.
```python

    player.play()
```

Alternatively, you can create a WinAQPlayer to play AudioQuantums. Similarly to [Luke Stack's aqplayer]

```python

    audio_file = audio.LocalAudioFile("test_file.mp3")
    bars = audio_file.analysis.bars

    player = wp.WinAQPlayer(audio_file)

    for bar in bars:
        player.add_audio(bar)

    player.play()
```




**Code Explanation**

The WinPlayer works on its own thread: a PlayThread. This functions off one key function: the run() function.

```python

    def run(self):
            while True:
                if self.play_event.is_set():
                    next_audio = self.player.get_next_audio()
                    print("Playing " + next_audio)
                    winsound.PlaySound(next_audio, winsound.SND_FILENAME)
                else:
                    self.play_event.wait()
```

Each iteration of the loop (which will run until the thread is closed), the thread will check an internal play_event to see if it's set. I encoded this Event to be able to handle pausing of the player. Basically, when the even is set, the player plays as normal. When the event is cleared, we wait until the event value is changed (the player is unpaused). I will build more off of this in a future revision.

The thread will get the next audio file to play from the player. Because the Queue is initialized by default with blocking enabled, it will wait until something is added to the queue. So if the player is "playing" with nothing on the queue, you will hear audio the instance you add another track to the queue.

The WinAQPlayer is a subclass of the WinPlayer. Basically it functions like this:

* Pass it the "master" WAV file of the AudioQuantums you want played in the constructor
* add_audio will create a WAV file of only the specified AudioQuantum, using the wave module
* add_audio then passes the newly created WAV file to the superclass's (WinPlayer's) add_audio method
* that quantum is now queued up for play.

```python

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
```

The WinAQPlayer currently uses a local temporary directory that holds the intermediary WAV files. They are deleted as they are played. This may change in the future.



**Resources**

1. [Python - winsound Documentation]
2. [Luke Stack's aqplayer]

[Python - winsound Documentation]:https://docs.python.org/2/library/winsound.html
[Luke Stack's aqplayer]:https://github.com/jlstack/PythonEchonestRemix/tree/master/aqplayer
