import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
"""

Work in progress

"""

class SpotifyInfo:
    def __init__(self, client_id, secret):
        self.client_id = client_id
        self.secret = secret
    
    def authenticate(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.secret)
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    def get_tracks_info(self, album_list):
        pass
