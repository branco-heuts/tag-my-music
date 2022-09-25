from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from os import getenv
from parse import args

# ------ Load Spotify API credentials ------
load_dotenv()
REDIRECT_URI = getenv('REDIRECT_URI')
CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')


class SpotifyData(Spotify):
    def __init__(self):
        super().__init__()

        self.auth_manager = SpotifyOAuth(
            scope="user-library-read",
            redirect_uri=REDIRECT_URI,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            show_dialog=True
        )

        self.playlist_id = args.playlist  # Get Spotify playlists
        self.library_location = args.local  # Local library
        self.music_library = str(args.name)  # Get library name
        self.choose_a_genre = args.genres  # Lets you choose/change genres
        self.playlist = self.playlist(playlist_id=self.playlist_id)
        self.playlist_total_items = self.playlist['tracks']['total']

        # Spotify playlist tracks
        offset = 0
        limit = 100
        iterations = int(self.playlist_total_items / limit)
        self.playlist_music = []
        for i in range(0, iterations + 1):  # Loop through entire Spotify library in bins of 100 tracks
            subset_playlist_music = self.playlist_items(self.playlist_id,
                                                        limit=limit,
                                                        offset=offset,
                                                        fields='items,name,uri',
                                                        additional_types=['track'])
            self.playlist_music.extend(subset_playlist_music['items'])
            offset += limit
