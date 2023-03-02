import isodate
from googleapiclient.discovery import build
from datetime import datetime as dt


class YouTubeApi:
    def __init__(self, api_service_name, api_version, api_key):
        self.api_service_name = api_service_name
        self.api_version = api_version
        self.api_key = api_key

    def get_channels_response(self, channel_id_list):
        yt = build(self.api_service_name, self.api_version,
                   developerKey=self.api_key)
        request = yt.channels().list(part="snippet,contentDetails,statistics",
                                     id=','.join(channel_id_list))
        response = request.execute()
        return response["items"]

    def get_channels_info(self, channel_id_list):
        channels = self.get_channels_response(channel_id_list)
        return [
            {
                "channel_id": channel["id"],
                "playlist_id": channel["contentDetails"]["relatedPlaylists"]["uploads"],
                "channel_name": channel["snippet"]["localized"]["title"],
                "published_at": channel["snippet"]["publishedAt"],
            } for channel in channels
        ]

    def get_channels_stats(self, channel_id_list):
        channels = self.get_channels_response(channel_id_list)
        return [
            {
                "channel_id": channel["id"],
                "view_count": int(channel["statistics"]["viewCount"]),
                "subscriber_count": int(channel["statistics"]["subscriberCount"]),
                "video_count": int(channel["statistics"]["videoCount"]),
                "date": dt.now().date()
            } for channel in channels
        ]

    def get_videos_ids(self, playlist_id_list):
        yt = build(self.api_service_name, self.api_version,
                   developerKey=self.api_key)
        video_ids = []
        for playlist_id in playlist_id_list:
            request = yt.playlistItems().list(part="snippet,contentDetails",
                                              playlistId=playlist_id, maxResults=50)
            response = request.execute()
            video_ids += [el["contentDetails"]["videoId"]
                          for el in response["items"]]
            next_page_token = response.get('nextPageToken')
            while next_page_token is not None:
                request = yt.playlistItems().list(
                    part='contentDetails',
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token)
                response = request.execute()
                video_ids += [el["contentDetails"]["videoId"]
                              for el in response["items"]]
                next_page_token = response.get('nextPageToken')
        return video_ids

    def get_video_details(self, playlist_id_list):
        yt = build(self.api_service_name, self.api_version,
                   developerKey=self.api_key)
        video_ids = self.get_videos_ids(playlist_id_list)
        num = len(video_ids)//50 + 1
        g = 0
        response = []
        for i in range(1, num + 1):
            request = yt.videos().list(part="snippet,contentDetails",
                                       id=','.join(video_ids[g:g+50]))
            response += request.execute()["items"]
            g += 50

        return [
            {
                "video_id": video["id"],
                "channel_id": video["snippet"]["channelId"],
                "title": video["snippet"]["title"],
                "published_at": video["snippet"]["publishedAt"],
                "duration_seconds": isodate.parse_duration(video["contentDetails"]["duration"]).total_seconds()
            } for video in response
        ]

    def get_video_stats(self, playlist_id_list):
        yt = build(self.api_service_name, self.api_version,
                   developerKey=self.api_key)
        video_ids = self.get_videos_ids(playlist_id_list)
        num = len(video_ids)//50 + 1
        g = 0
        response = []
        for i in range(1, num + 1):
            request = yt.videos().list(part="snippet,statistics",
                                       id=','.join(video_ids[g:g+50]))
            response += request.execute()["items"]
            g += 50

        return [
            {
                "video_id": video["id"],
                "view_count": int(video["statistics"]["viewCount"]),
                "like_count": int(video["statistics"]["likeCount"]),
                "comment_count": int(video["statistics"]["commentCount"]),
                "date": dt.now().date()
            } for video in response
        ]
