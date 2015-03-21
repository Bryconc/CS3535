## Spotify Playlist Sampler - Synchronous ##

The application synchronously samples a public Spotify playlist. That is, it randomly grabs X amount of tracks from a public Spotify playlist and plays their samples in succession

**Process**

The application recieves as command-line input the Spotify user and their public playlist you wish to sample. It retrieves the information from Spotify about that playlist, then randomly selects X tracks from the playlist. It must download each of the track's 30 second samples. Then it must convert each to a WAV file via echonest analyzer. Finally, it plays each in succession. All is done synchronously so output time is slow.

**Dependencies**

At the moment this MUST be done on a Windows computer. Mac support will come later.

You also need a Spotify account as it will prompt you to log in to access public information.

To use spotify_playlist_sampler.py, you will need:

      - spotipy
      - echonest.remix

**Future Use**

This is the first step in my project. I next plan to turn this synchronous program into an asynchronous program that can process much more data.

**Example**

Execute spotify_playlist_sampler.py with a Spotify username and their playlist. This can be found in the url of the playlist.

```
    python spotify_playlist_sampler.py george_spv 6nhiBJot8yHf2BHoRrBUmJ
```

The first time executing this program you will likely be prompted to login with your Spotify credentials. This should only happen seldomly. After much computation time the
samples will be played in a random order.

**Code Explanation**

As a preliminary, in order to access certain Spotify information - denoted in the Spotipy documentation - you need to present it with user authentication. I generated my key information through the Spotify website, registering my application.

```python
    token = util.prompt_for_user_token(user, client_id="1e9958fdd24746aea8959ccf6f724441", client_secret="a5bcdc07002c463f87a7d827c1638b91", redirect_uri="http://www.google.com")
    if token:
        sp = spotipy.Spotify(auth=token)
```

This will initially require you to login to Spotify but you should be fine after that.

For this application we're going to access the public Spotify playlist via the user that created it. That can be done through a method in spotipy.

```python
    playlist = sp.user_playlist(user, playlist_id)
```

Now we need to get the tracks from the playlist Object returned via the previous method.

```python

    tracks = playlist["tracks"]

    add_tracks(tracks)

    while tracks["next"]:
        tracks = sp.next(tracks)
        add_tracks(tracks)
```

The tracks are only stored in lists of 100 at a time, so once we process 100 of them we need to advance to the "next" list. Though this we have added all of the tracks with preview urls to a master tracklist.

Now we begin to the local playlist of sampled files. But before we can play anything we need a WAV file. And all we have at the moment is a URL to the preview MP3. So we're going to have to go some work.

```python

    def add_sampled_tracks():
        for i in range(TEST_SIZE):
            index = random.randint(0, len(master_track_list) - 1)
            track = master_track_list[index]
            master_track_list.remove(track)
            track_list.append(track)
            print("%d. Added %s" % (len(track_list), track['track']['name']))
            print("Downloading %s" % track['track']['preview_url'])
            mp3file, headers = urllib.urlretrieve(track['track']['preview_url'], "test.mp3")
            samples.append(audio.LocalAudioFile(mp3file))
```

As a constant, this synchronous player will limit itself to TEST_SIZE samples. Adjust this number to your needs.

First we grad a random track from the master track playlist. Then we access its 'preview_url' and use the 'urlretrieve' method to download the MP3 at that location. We store the retrieved URL in an intermediary 'test.mp3' file.
We then append a LocalAudioFile object of that MP3 to the samples list. This indirectly created a WAV representation of the audio, and we no longer need the test.mp3 for that track.

Finally, once we've downloaded and converted everything to WAV files we're ready to start playing.

This is done in a simple loop of getting the track and sample file. And passing it to the winsound playSound method.
```python

    while samples:
            index = random.randint(0, len(track_list) - 1)
            sample = samples[index]
            samples.remove(sample)
            track = track_list[index]
            track_list.remove(track)
            print("Playing %s - %s" % (track["track"]["name"], track["track"]["artists"][0]["name"]))
            winsound.PlaySound(get_wav(sample), winsound.SND_FILENAME)
```


**Resources**

1. [Spotify App Registration]
2. [Spotipy Documentation]
3. [Python - winsound Documentation]

[Spotify App Registration]: https://developer.spotify.com/my-applications/
[Spotipy Documentation]: https://media.readthedocs.org/pdf/spotipy/latest/spotipy.pdf
[Python - winsound Documentation]: https://docs.python.org/2/library/winsound.html