from os import environ, getcwd
import psycopg2 as ps
import datetime
from get_spotify_stats import SpotifyAPI
from yt_api_handling import YouTubeApi
from sql_handling import Database as DB


api_service_name = "youtube"
api_version = "v3"
api_key = environ.get("youtube_api_key")
spotify_username = environ.get("spotify_login")
spotify_password = environ.get("spotify_password")


with open(f"spotify_with_yt\\getting_data\\channels.txt", "r") as f:
    channels = [element.split(",")[0] for element in f.read().split("\n")]

with open("spotify_with_yt\\getting_data\\artists.txt", "r") as f:
    artists = [element.split(",")[0] for element in f.read().split("\n")]


with open("spotify_with_yt\\getting_data\\albums.txt", "r") as f:
    albums = [element.split(",")[0] for element in f.read().split("\n")]


youtube = YouTubeApi(api_service_name, api_version, api_key)
spotify = SpotifyAPI(spotify_username, spotify_password)

channels_info = youtube.get_channels_info(channels)
channels_stats = youtube.get_channels_stats(channels)
videos_info = youtube.get_video_details([el["playlist_id"] for el in channels_info])
videos_stats = youtube.get_video_stats([el["playlist_id"] for el in channels_info])
bearer = spotify.get_bearer_token()
artists = spotify.get_artists(artists, bearer)
albums_info = spotify.get_albums_info(albums, bearer)
songs_info = spotify.get_songs_info(albums, bearer)
songs_stats = spotify.get_songs_stats(albums, bearer)


dbname = "spotify_and_yt"
port = 5433
username = "postgres"
sql_password = environ.get("postgres_passwd")

db = DB(dbname, port, username, sql_password)
conn = ps.connect(
    f"dbname={dbname} user={username} password={sql_password} port={port}")

with conn.cursor() as curr:
    db.create_channels_info_table(curr)
    db.create_channels_stats_table(curr)
    db.create_videos_info_table(curr)
    db.create_videos_stats_table(curr)
    db.create_artists_table(curr)
    db.create_albums_table(curr)
    db.create_songs_info_table(curr)
    db.create_songs_stats_table(curr)

    db.append_channels_info_table(curr, channels_info)
    db.append_channels_stats_table(curr, channels_stats)
    db.append_videos_info_table(curr, videos_info)
    db.append_videos_stats_table(curr, videos_stats)
    db.append_artists_table(curr, artists)
    db.append_albums_table(curr, albums_info)
    db.append_songs_info_table(curr, songs_info)
    db.append_songs_stats_table(curr, songs_stats)
    conn.commit()
