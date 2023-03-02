import psycopg2 as ps


class Database:
    def __init__(self, dbname, port, username, password):
        self.dbname = dbname
        self.port = port
        self.username = username
        self.password = password

    def create_channels_info_table(self, curr):
        create_table_command = ("""CREATE TABLE IF NOT EXISTS channels_info (
                        channel_id VARCHAR(255),
                        playlist_id VARCHAR(255),
                        channel_name VARCHAR(255),
                        published_at DATE,
                        PRIMARY KEY (channel_id)
                );""")
        curr.execute(create_table_command)

    def create_channels_stats_table(self, curr):
        create_table_command = ("""CREATE TABLE IF NOT EXISTS channels_stats(
                        channel_id VARCHAR(255),
                        view_count BIGINT,
                        subscriber_count BIGINT,
                        video_count INTEGER,
                        date DATE,
                        PRIMARY KEY (channel_id, date)
                );""")
        curr.execute(create_table_command)

    def create_videos_info_table(self, curr):
        create_table_command = ("""CREATE TABLE IF NOT EXISTS videos_info (
                        video_id VARCHAR(255),
                        channel_id VARCHAR(255),
                        title VARCHAR(255),
                        published_at DATE,
                        duration_seconds DECIMAL,
                        PRIMARY KEY (video_id)
                );""")
        curr.execute(create_table_command)

    def create_videos_stats_table(self, curr):
        create_table_command = ("""CREATE TABLE IF NOT EXISTS videos_stats (
                        video_id VARCHAR(255),
                        view_count DECIMAL,
                        like_count DECIMAL,
                        comment_count DECIMAL,
                        date DATE,
                        PRIMARY KEY (video_id, date)
                );""")
        curr.execute(create_table_command)

    def create_artists_table(self, curr):
        create_table_command = ("""CREATE TABLE IF NOT EXISTS artists (
                        artist_id VARCHAR(255),
                        name VARCHAR(255),
                        followers DECIMAL,
                        monthly_listeners DECIMAL,
                        date DATE,
                        PRIMARY KEY (artist_id, date)
                );""")
        curr.execute(create_table_command)

    def create_albums_table(self, curr):
        create_table_command = ("""CREATE TABLE IF NOT EXISTS albums (
                        album_id VARCHAR(255),
                        name VARCHAR(255),
                        release DATE,
                        label VARCHAR(255),
                        artists TEXT,
                        PRIMARY KEY (album_id)  
                );""")
        curr.execute(create_table_command)

    def create_songs_info_table(self, curr):
        create_table_command = ("""CREATE TABLE IF NOT EXISTS songs_info (
                        album_id VARCHAR(255),
                        track_id VARCHAR(255),
                        name VARCHAR(255),
                        duration_ms DECIMAL,
                        artists TEXT,
                        PRIMARY KEY (track_id)
                );""")
        curr.execute(create_table_command)

    def create_songs_stats_table(self, curr):
        create_table_command = ("""CREATE TABLE IF NOT EXISTS songs_stats (
                        track_id VARCHAR(255),
                        playcount DECIMAL,
                        date DATE,
                        PRIMARY KEY (track_id, date)
                );""")
        curr.execute(create_table_command)

    def insert_into_channels_info_table(self, curr, channel_id, playlist_id, channel_name, published_at):
        insert_command = ("""INSERT INTO channels_info (channel_id, playlist_id, channel_name, published_at)
        VALUES(%s,%s,%s,%s);""")
        row_to_insert = (channel_id, playlist_id, channel_name, published_at)
        curr.execute(insert_command, row_to_insert)

    def insert_into_channels_stats_table(self, curr, channel_id, view_count, subscriber_count, video_count, date):
        insert_command = ("""INSERT INTO channels_stats (channel_id, view_count, subscriber_count, video_count, date)
        VALUES(%s,%s,%s,%s,%s);""")
        row_to_insert = (channel_id, view_count,
                         subscriber_count, video_count, date)
        curr.execute(insert_command, row_to_insert)

    def insert_into_videos_info_table(self, curr, video_id, channel_id, title, published_at, duration_seconds):
        insert_command = ("""INSERT INTO videos_info (video_id, channel_id, title, published_at, duration_seconds)
        VALUES(%s,%s,%s,%s,%s);""")
        row_to_insert = (video_id, channel_id, title,
                         published_at, duration_seconds)
        curr.execute(insert_command, row_to_insert)

    def insert_into_videos_stats_table(self, curr, video_id, view_count, like_count, comment_count, date):
        insert_command = ("""INSERT INTO videos_stats(video_id, view_count, like_count, comment_count, date)
        VALUES(%s,%s,%s,%s,%s);""")
        row_to_insert = (video_id, view_count, like_count, comment_count, date)
        curr.execute(insert_command, row_to_insert)

    def insert_into_artists_table(self, curr, artist_id, name, followers, montly_listeners, date):
        insert_command = ("""INSERT INTO artists (artist_id, name, followers, monthly_listeners, date)
        VALUES(%s,%s,%s,%s,%s);""")
        row_to_insert = (artist_id, name, followers, montly_listeners, date)
        curr.execute(insert_command, row_to_insert)

    def insert_into_albums_table(self, curr, album_id, name, release, label, artists):
        insert_command = ("""INSERT INTO albums (album_id, name, release, label, artists)
        VALUES(%s,%s,%s,%s,%s);""")
        row_to_insert = (album_id, name, release, label, artists)
        curr.execute(insert_command, row_to_insert)

    def insert_into_songs_info_table(self, curr, album_id, track_id, name, duration_ms, artists):
        insert_command = ("""INSERT INTO songs_info (album_id, track_id, name, duration_ms, artists)
        VALUES(%s,%s,%s,%s,%s);""")
        row_to_insert = (album_id, track_id, name, duration_ms, artists)
        curr.execute(insert_command, row_to_insert)

    def insert_into_songs_stats_table(self, curr, track_id, playcount, date):
        insert_command = ("""INSERT INTO songs_stats (track_id, playcount, date)
        VALUES(%s,%s,%s);""")
        row_to_insert = (track_id, playcount, date)
        curr.execute(insert_command, row_to_insert)

    def check_if_channel_exists(self, curr, channel_id):
        query = ("SELECT channel_id FROM channels_info WHERE channel_id = %s;")
        curr.execute(query, (channel_id,))
        return curr.fetchone() is not None

    def check_if_video_exists(self, curr, video_id):
        query = ("SELECT video_id FROM videos_info WHERE video_id = %s;")
        curr.execute(query, (video_id,))
        return curr.fetchone() is not None

    def check_if_album_exists(self, curr, album_id):
        query = ("SELECT album_id FROM albums WHERE album_id = %s;")
        curr.execute(query, (album_id,))
        return curr.fetchone() is not None

    def check_if_song_exists(self, curr, track_id):
        query = ("SELECT track_id FROM songs_info WHERE track_id = %s;")
        curr.execute(query, (track_id,))
        return curr.fetchone() is not None

    def append_channels_info_table(self, curr, list_of_dicts):
        for element in list_of_dicts:
            if not self.check_if_channel_exists(curr, element["channel_id"]):
                self.insert_into_channels_info_table(
                    curr, element["channel_id"], element["playlist_id"], element["channel_name"], element["published_at"])

    def append_channels_stats_table(self, curr, list_of_dicts):
        for element in list_of_dicts:
            self.insert_into_channels_stats_table(
                curr, element["channel_id"], element["view_count"], element["subscriber_count"], element["video_count"], element["date"])

    def append_videos_info_table(self, curr, list_of_dicts):
        for element in list_of_dicts:
            if not self.check_if_video_exists(curr, element["video_id"]):
                self.insert_into_videos_info_table(
                    curr, element["video_id"], element["channel_id"], element["title"], element["published_at"], element["duration_seconds"])

    def append_videos_stats_table(self, curr, list_of_dicts):
        for element in list_of_dicts:
            self.insert_into_videos_stats_table(
                curr, element["video_id"], element["view_count"], element["like_count"], element["comment_count"], element["date"])

    def append_artists_table(self, curr, list_of_dicts):
        for element in list_of_dicts:
            self.insert_into_artists_table(
                curr, element["artist_id"], element["name"], element["followers"], element["monthly_listeners"], element["date"],)

    def append_albums_table(self, curr, list_of_dicts):
        for element in list_of_dicts:
            if not self.check_if_album_exists(curr, element["album_id"]):
                self.insert_into_albums_table(
                    curr, element["album_id"], element["name"], element["release"], element["label"], str(element["artists"]))

    def append_songs_info_table(self, curr, list_of_dicts):
        for element in list_of_dicts:
            if not self.check_if_song_exists(curr, element["track_id"]):
                self.insert_into_songs_info_table(
                    curr, element["album_id"], element["track_id"], element["name"], element["duration_ms"], str(element["artists"]))

    def append_songs_stats_table(self, curr, list_of_dicts):
        for element in list_of_dicts:
            self.insert_into_songs_stats_table(
                curr, element["track_id"], element["playcount"], element["date"])
