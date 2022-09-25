from spotify_data import SpotifyData
from music_tag import load_file
from urllib.request import urlretrieve
from tqdm import tqdm
from genre_gui import App
from re import sub
from os import listdir, remove
from pathlib import Path

sp = SpotifyData()


def add_metadata(track, id3_tags):
    """
    For each track, edit and add Spotify's metadata to each file (.mp3/.wav).

    WARNING: there is currently a bug when added metadata to .wav files. The data gets adding, but doesn't update
    properly. To fix this, you need to manually update an ID3 tag of choice. This can easily be done using the 'mp3tag'
    program. I recommend updating a tag that you will not use, in my case that would be 'Discnumber'.

    - Title
    - Artists
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

    :param track: Music file name, without extension.
    :param id3_tags: id3_object (music-tag library)
    """




# -------------------------------------- Spotify custom playlist library -----------------------------------------------

# Create nested dictionary from sp.playlist_items()
print("> Creating Spotify music metadata dictionary")
music_dict = {}
for n in range(0, len(sp.playlist_music)):

    # Uri
    uri = sp.playlist_music[n]['track']['uri']

    # Title
    track_title = sp.playlist_music[n]['track']['name']
    if " - " in track_title:  # reformat remix titles etc.
        track_title = track_title.replace("- ", "(") + ")"

    # Artists
    n_contributing_artists = len(sp.playlist_music[n]['track']['artists'])
    contributing_artists = [sp.playlist_music[n]['track']['artists'][x]['name'] for x in
                            range(0, n_contributing_artists)]
    contributing_artists_joined = ', '.join(contributing_artists)
    artists_and_title = contributing_artists_joined + " - " + track_title

    # Deal with illegal characters
    illegal_characters = '\/:*?"<>|'
    char_list = [c for c in artists_and_title if c in illegal_characters]
    char_list = list(dict.fromkeys(char_list))  # Remove duplicates from list
    for c in char_list:
        artists_and_title = artists_and_title.replace(c, '')
    artists_and_title = sub(' +', ' ', artists_and_title)  # Remove double spaces

    music_dict.update(
        {
            artists_and_title:
                {
                    "uri": uri,
                    "artist_id": sp.playlist_music[n]['track']['artists'][0]['id'],  # Take first artist
                    "album_id": sp.playlist_music[n]['track']['album']['id'],
                    "album_name": sp.playlist_music[n]['track']['album']['name'],
                    "album_type": sp.playlist_music[n]['track']['album']['album_type'],
                    "release_date_album": sp.playlist_music[n]['track']['album']['release_date'],
                    "release_date_precision": sp.playlist_music[n]['track']['album']['release_date_precision'],
                    "img_url": sp.playlist_music[n]['track']['album']['images'][0]['url'],
                    "preview_url": sp.playlist_music[n]['track']['preview_url'],
                    "popularity": sp.playlist_music[n]['track']['popularity'],
                    "artists": contributing_artists_joined,
                    "tracktitle": track_title,

                }
        }
    )

# print(music_dict)

# ---------------------- Match local with Spotify library, get audio features, and add ID3 tags ------------------------

print("> Matching... Getting audio features... Adding ID3 tags... \n")
missing_in_spotify_playlist = []
for file in tqdm(listdir(sp.library_location)):
    path_to_file = sp.library_location + "/" + str(file)
    if str(path_to_file).split(".")[-1] != "mp3" and str(path_to_file).split(".")[-1] != "wav":
        continue  # Skip all files except .mp3 or .wav
    id3_object = load_file(path_to_file)  # music_tag library
    track_name = Path(path_to_file).stem

    # Spotify names
    # Filenames need to match 100% with the corresponding track name in your Spotify playlist.
    if track_name in music_dict.keys():
        track=track_name
        id3_tags=id3_object
        audio_features = sp.audio_features(tracks=music_dict[track]['uri'])

        # Add title
        id3_tags['tracktitle'] = music_dict[track]['tracktitle']

        # Add artists
        id3_tags['artist'] = music_dict[track]['artists']

        # Add comments
        try:
            id3_tags['comment'] = f"/* Library: {sp.music_library} " \
                                  f"/* Popularity: {music_dict[track]['popularity']} " \
                                  f"/* Danceability: {audio_features[0]['danceability']} " \
                                  f"/ Energy: {audio_features[0]['energy']} " \
                                  f"/ Happiness: {audio_features[0]['valence']} " \
                                  f"/ Instrumentalness: {audio_features[0]['instrumentalness']} " \
                                  f"/ Acousticness: {audio_features[0]['acousticness']} " \
                                  f"/ Speechiness: {audio_features[0]['speechiness']} " \
                                  f"/ Liveness: {audio_features[0]['liveness']} " \
                                  f"/ Loudness: {audio_features[0]['loudness']} " \
                                  f"/ Tempo: {audio_features[0]['tempo']} " \
                                  f"/ Key: {audio_features[0]['key']} */"
        except TypeError:
            print(f"\tSomething went wrong... No audiofeatures found for: {track}")
            id3_tags['comment'] = "None"

        # Add album
        if music_dict[track]['album_type'] == "album":  # Else album_type will be called "Single"
            music_dict[track]['album_type'] = music_dict[track]['album_name']
        id3_tags['album'] = music_dict[track]['album_type']

        # Add release date
        if music_dict[track]['release_date_precision'] == 'year':
            id3_tags['year'] = music_dict[track]['release_date_album'] + "-01-01"
        elif music_dict[track]['release_date_precision'] == 'month':
            id3_tags['year'] = music_dict[track]['release_date_album'] + "-01"
        else:
            id3_tags['year'] = music_dict[track]['release_date_album']

        # Add Genre
        additional_album_info = sp.album(album_id=music_dict[track]['album_id'])
        if additional_album_info['genres']:  # Get album genre if possible
            genre_list = additional_album_info['genres']
        else:  # Otherwise get artist genre (list)
            artist_info = sp.artist(artist_id=music_dict[track]['artist_id'])
            genre_list = artist_info['genres']

        if sp.choose_a_genre:
            preview_and_choose = App(track=track,
                                     preview_url=music_dict[track]['preview_url'],
                                     genre_list=genre_list)
            id3_tags['genre'] = preview_and_choose.picked_genre
        else:
            id3_tags['genre'] = genre_list

        # Artwork
        save_name = "./artwork_image.jfif"
        urlretrieve(music_dict[track]['img_url'], save_name)
        with open(save_name, 'rb') as img_in:
            id3_tags['artwork'] = img_in.read()
        art = id3_tags['artwork']
        art.first.thumbnail([64, 64])

        id3_tags.save()
    else:
        missing_in_spotify_playlist.append(track_name)
