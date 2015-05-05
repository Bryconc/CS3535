## Spotify Playlist Sampler - Asynchronous ##

The application asynchronously samples a public Spotify playlist. That is, it randomly grabs X amount of tracks from a public Spotify playlist and plays their samples in succession. The application now supports threading.

**Process**

The application now works in a threaded manner. The tracks will queue up, download, analyze, and play in respective threads. The application should now be able to process any sized playlist within a 4-5 second startup time.

The application works off a pipeline process like so.

<img src="https://github.com/Bryconc/CS3535/blob/master/Research%20Module%204%20-%20Spotify%20Playlist%20Sampler%20Asynchronous/Sampler%20Pipeline.png?raw=true">

**Dependencies**

At the moment this MUST be done on a Windows computer. Mac support will come later.

You also need a Spotify account as it will prompt you to log in to access public information.

To use spotify_playlist_sampler.py, you will need:

      - spotipy
      - echonest.remix

**Future Use**

Now that my application is threaded. I will seek to apply a GUI, making it interactive and infinitely expanding its possibilities.

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

Now we begin to the local playlist of sampled files. But before we can play anything we need a WAV file. And all we have at the moment is a URL to the preview MP3. So we're going to have to do some work.

First we initiate the new Thread objects like so:

```python

    amount = len(master_track_list)
    player = wp.WinPlayer()
    analyzer = AnalyzerThread(player, amount)
    downloader = DownloaderThread(analyzer, amount)

    downloader.start()
    analyzer.start()

    player.play()
```

All threads will be initialized and awaiting queued tracks.

All that remains to be done is begin queueing up the tracks for download and the pipeline will take care of the rest.

```python

    for i in range(len(master_track_list)):
        index = random.randint(0, len(master_track_list) - 1)
        track = master_track_list[index]
        master_track_list.remove(track)
        track_list.append(track)
        downloader.queue_download(track)


**Resources**

1. [Spotify App Registration]
2. [Spotipy Documentation]
3. [Python - winsound Documentation]

[Spotify App Registration]: https://developer.spotify.com/my-applications/
[Spotipy Documentation]: https://media.readthedocs.org/pdf/spotipy/latest/spotipy.pdf
[Python - winsound Documentation]: https://docs.python.org/2/library/winsound.html
