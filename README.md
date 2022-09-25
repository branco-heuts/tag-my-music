# TagMyMusic
Lets you add a bunch of Spotify's track metadata to your music files (MP3/WAV):

- Title
- Artist(s)
- Comments
    - Library name
    - Popularity
    - Danceability
    - Energy
    - Happiness
    - Instrumentalness
    - Acousticness
    - Speechiness
    - Liveness
    - Loudness
    - Tempo
    - Key
- Album
- Release date
- Genre (artist or album)
- Artwork

<i>WARNING: there is currently a bug when adding metadata to .wav files. The data gets added, but doesn't update
    properly. To fix this, you need to manually update any ID3 tag of choice. This can easily be done using the 'mp3tag'
    program. I recommend updating a tag that you will not use, in my case that would be 'Discnumber'.</i>

## Installation
Clone this project to your IDE of choice.
```bash
  git clone https://github.com/branco-heuts/tag-my-music.git
```

## Usage 
#### Spotify credentials
You need to setup <u>your own Spotify Dashboard App</u> for this to work. In order to do this, you can use a lightweight Python library for the Spotify Web API, <i>spotipy</i>. You need to setup Spotify authentication to to allow third-party applications.

##### Here is how:
1. Go to [your Spotify for Developers Dashboard](https://developer.spotify.com/dashboard/)
2. Log in to your Spotify account
3. Create an App
4. Go to '<b>Edit Settings</b>'
5. Add 'http://example.com' to '<b>Redirect URIs</b>'
6. Click '<b>Add</b>'
7. Copy and paste 'Client ID' and 'Client Secret' to .env ([example]())
8. Run tagmymusic.py
9. If Spotify authentication was successful, you should see a Spotify page asking you to agree to their terms.
10. Click Agree
11. Copy <u><b>the entire URL</u></b> and paste it into the prompt of your IDE (I use PyCharm here)
12. Close and restart your IDE.
13. All done!

#### Terminal
You have to provide the following:
1. A link to your Spotify playlist 
2. Path to your local music directory 
3. Library name that fits your music

Make sure to (re)name your local MP3/WAV files according to their respective track name that is displayed on Spotify. <strong>It's important that your local files <u>match exactly</u> with the track names in your Spotify playlist.</strong> To aid you in this process, two files will be generated after running tagmymusic.py:
* 1_tracks_missing_in_local_library_YOUR-LIBRARY.txt<br></br>

    <i>Gives you a list of track names that is missing in your local music library. This will include all files that don't exactly match compared to the tracks in your Spotify playlist.</i>


* 2_tracks_missing_in_spotify_playlist_YOUR-LIBRARY.txt<br></br>

    <i>Gives you a list of tracks that are in your local music library, but missing in your Spotify playlist.</i>
<br></br>

##### Run the command in the terminal
For example:
```bash
python .\tagmymusic\tagmymusic.py -p https://open.spotify.com/playlist/37i9dQZF1DWWvhKV4FBciw?si=41fe8645ca7e4ed6 -l "C:\Users\User1\Music\Funk" -n Funk
```

## Genre
Adding a genre is a bit of a weird one. Spotify does not offer you the genre that is associated with the track of your choice. Instead, Spotify can give you a genre for an artist's album (sometimes), or all the genres associated to a certain artist. If neither information is available, there will be no genre added to you track of choice. In most cases, there will be a list of genres given to your track. In reality this is not really useful. Therefore, you will have the option to curate the genres of your music library as the metadata gets added to your tracks.

##### How does this work?
You can provide the '-g' or '--genres' flag to your tagmymusic.py command, like so:
```bash
python tagmymusic.py -p https://open.spotify.com/playlist/37i9dQZF1DWWvhKV4FBciw?si=41fe8645ca7e4ed6 -l "C:\Users\User1\Music\Funk" -n Funk --genres
```

If possible, a window will pop up that lets you:
* see the (list of) genres associated to the artist/album;
* hear a 30 second audio fragment from the respective track;
* pick a genre from the list;
* or write your own genre.
