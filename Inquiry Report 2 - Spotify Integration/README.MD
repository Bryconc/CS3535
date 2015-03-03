# Problem #
We want to be able to integrate Spotify with our applications.

# Questions #
1. How can we connect our application to Spotify?
2. How can we utilize this through Python?
3. What potential uses can Spotify integration give us?

# Resources #
1. [Spotify Partnership Information]/[Echonest - Spotify Overview]
2. [Spotipy Documentation]
3. [Echonest-Spotify Examples GitHub Repo]

### Mini-abstract and relevance of [Spotify Partnership Information]/[Echonest - Spotify Overview]  ###

A year ago, Echo Nest was aquired by Spotify. This allowed for major integration between the two APIs and development of some powerful applications. There is a key way you can modify your Echo Nest queries to get Spotify oriented results. Simply denote the 'id' value of your request URL to 'spotify'.

As an example, with the following request URL we can retrieve the biographies for the artist Radiohead.

```
    http://developer.echonest.com/api/v4/artist/biographies?api_key=FILDTEOIK2HBORODV&id=spotify:artist:4Z8W4fKeB5YxbusRsdQVPb
```

Note specifically the "spotify:artist:4Z8W4fKeB5YxbusRsdQVPb" portion of the URL. This is Radiohead's specific id in the Spotify Catalog. A quick look in the [Spotify Developer's Web API User Guide] shows us that this information can be easily obtained "by right-clicking on the artist's or album's or track's name" from within the Spotify application.

Alternatively, we can obtain the information for Spotify IDs by appending the parameter "bucket=id:spotify" As an example, to find artists similar to Radiohead, with Spotify foreign IDs returned, we would issue this request

```
    http://developer.echonest.com/api/v4/artist/similar?api_key=YOUR_API_KEY&id=spotify:artist:4Z8W4fKeB5YxbusRsdQVPb&bucket=id:spotify
```

Which will return the output like so:

```json

    {
        "foreign_ids": [
            {
                "catalog": "spotify",
                "foreign_id": "spotify:artist:4CvTDPKA6W06DRfBnZKrau"
            }
        ],
        "id": "ARH1N081187B9AC562",
        "name": "Thom Yorke"
    }
```

And as you can see, the Spotify ID for artist Thom Yorke would be "spotify:artist:4CvTDPKA6W06DRfBnZKrau"

### Mini-abstract and relevance of [Spotipy Documentation] ###

Though Echonest provides useful features with Spotify, for our purposes it would be nice to have a Python module to do most of the work. That's where Spotipy comes in! Spotipy is a compact Python library for the Spotify Web API. Spotipy provides all the music data provided by the Spotify platform in a lightweight manner. Though the [Spotipy API] would be the best manner to learn this nice module, an example would be a nice start. For any deeper understanding it is also helpful to investigate the source code on [Spotipy GitHub].

```python

    import spotipy

    birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
    spotify = spotipy.Spotify()

    results = spotify.artist_albums(birdy_uri, album_type='album')
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    for album in albums:
        print(album['name'])
```

The above is a simple script to list all the albums released by the artist 'Birdy'.

A few important things to understand about the example:

* The pivotal thing to understand when working with Spotify development is the concept of the Spotify URLs, like I explained a little in the previous section; this is elaborated on again on the Spotipy website under the heading [IDs URIs and URLs]. Just understand that every artist, album, and track have specific IDs assigned to them in the Spotify catalog, and that's how you reference them.
* It is crucial to create an instance of the Spotify() object. This is the Object which will perform request calls to the Spotify Web API.

### Mini-abstract and relevance of [Echonest-Spotify Examples GitHub Repo] ###

Finally we come to some larger, practical applications. Here we have a GitHub Repo sponsored by the creators of Echonest that show some interesting examples using Spotify integration. Specifically of interest is the "python" directory. Here we will look at their first example, example1.py.

```python

    import pyen
    import spotipy
    import sys

    '''
     get a set of images for artists that are similar to
     the given seed artist
    '''

    en = pyen.Pyen()
    sp = spotipy.Spotify()

    name = 'weezer'
    if len(sys.argv) > 1:
        name = ' '.join(sys.argv[1:])

    spids = []
    response = en.get('artist/similar', name=name, bucket='id:spotify', limit=True)
    for artist in response['artists']:
        spids.append(artist['foreign_ids'][0]['foreign_id'])

    for artist in sp.artists(spids)['artists']:
        print artist['images'][0]['url'], artist['name']
```

A few things to note about the example:

* The developers utilize a "pyen" module rather than using "pyechonest". The "pyen" module can be examined in-depth on the [pyen GitHub]. This module differs from "pyechonest" in that "it doesn't try to represent Echo Nest items such as artists, songs and tracks as objects. Instead, it just lets you call the API method and gives you back a dictionary representation of the Echo Nest response." This is friendly towards our spotipy module.
* Notice how, once the API call has been made to the "en" object, the following loop goes through the resulting object and accumulates all the ```artist['foreign_ids'][0]['foreign_id']``` values into the spids List. This accumulating those Spotify IDs that we've been dealing with so much!


[Spotify Partnership Information]:http://developer.echonest.com/sandbox/spotify.html
[Echonest - Spotify Overview]:http://static.echonest.com/enspex/
[Spotify Developer's Web API User Guide]:https://developer.spotify.com/web-api/user-guide/
[Spotipy Documentation]:http://spotipy.readthedocs.org/en/latest/#
[Spotipy API]:http://spotipy.readthedocs.org/en/latest/#api-reference
[Spotipy GitHub]:https://github.com/plamere/spotipy/tree/master/spotipy
[IDs URIs and URLs]:http://spotipy.readthedocs.org/en/latest/#ids-uris-and-urls
[Echonest-Spotify Examples GitHub Repo]:https://github.com/plamere/enspex
[pyen GitHub]:https://github.com/plamere/pyen