## Spotify Playlist Sampler with GUI ##

The application has advanced to display a GUI with current state of the player. The user can interact with the player by pausing and playing

**Process**

The process runs identical to the previous Sampler. The GUI was embeded within the WinPlayer class, so no functionality needed to change.

**Dependencies**

The module utilizes my WinPlayer that has been modified to support the GUI application. The directory still needs to contain a Temp_Directory folder for caching

**Future Use**

There are many things I wish to improve upon this application with:

* The code is very tightly coupled, and I wish to implement the Model View Control Pattern with it
* The application only supports the playlist it was initalized with. I wish to make it variable
* I want to add more functionality for exporting favorited tracks to a Spotify playlist. As of now, the menu options are there for place holders.

