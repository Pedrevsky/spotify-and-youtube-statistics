import json
import time
import requests
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs


class SpotifyAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_bearer_token(self):
        url = "https://open.spotify.com/"
        login = "https://accounts.spotify.com/pl/login?continue=https%3A%2F%2Fopen.spotify.com%2F"

        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()))
        driver.get(login)
        username_field = driver.find_element(By.ID, "login-username")
        password_field = driver.find_element(By.ID, "login-password")

        username_field.send_keys(self.username)
        password_field.send_keys(self.password)

        button = driver.find_element(By.ID, "login-button")
        button.click()

        time.sleep(5)

        driver.get(url)
        source = driver.page_source

        soup = bs(source, features="lxml")
        return json.loads(soup.find("script", {"id": "session"}).text)["accessToken"]

    def get_artists(self, artists_list, token):
        url_query = "https://api-partner.spotify.com/pathfinder/v1/query"
        # token = self.get_bearer_token()
        headers = {"authorization": f"Bearer {token}"}
        info = []
        for artist in artists_list:
            var = '{"uri":"spotify:artist:' + artist + '","locale":""}'
            querystring = {"operationName": "queryArtistOverview", "variables": var,
                           "extensions": "{\"persistedQuery\":{\"sha256Hash\":\"b82fd661d09d47afff0d0239b165e01c7b21926923064ecc7e63f0cde2b12f4e\"}}"}
            artist = json.loads(requests.get(url_query, headers=headers, params=querystring).text)
            artist = artist["data"]["artistUnion"]
            info.append({
                "artist_id": artist["id"],
                "name": artist["profile"]["name"],
                "followers": artist["stats"]["followers"],
                "monthly_listeners": artist["stats"]["monthlyListeners"],
                "date": dt.now().date()
            })

        return info

    def get_albums_info(self, albums_list, token):
        url_query = "https://api-partner.spotify.com/pathfinder/v1/query"
        # token = self.get_bearer_token()
        headers = {"authorization": f"Bearer {token}"}
        info = []
        for album in albums_list:
            var = '{"uri":"spotify:album:' + album + '","locale":""}'
            querystring = {"operationName": "getAlbumMetadata", "variables": var,
                           "extensions": "{\"persistedQuery\":{\"sha256Hash\":\"411f31a2759bcb644bf85c58d2f227ca33a06d30fbb0b49d0f6f264fda05ecd8\"}}"}
            raw_album = json.loads(requests.get(url_query, headers=headers, params=querystring).text)
            raw_album = raw_album["data"]["albumUnion"]

            info.append(
                {
                    "album_id": raw_album["uri"].split(":")[2],
                    "name": raw_album["name"],
                    "release": dt.strptime(raw_album["date"]["isoString"].split("T")[0], "%Y-%m-%d").date(),
                    "label": raw_album["label"],
                    "artists": [{"id": el["id"], "name": el["profile"]["name"]} for el in raw_album["artists"]["items"]]
                }
            )

        return info

    def get_songs_info(self, albums_list, token):
        url_query = "https://api-partner.spotify.com/pathfinder/v1/query"
        # token = self.get_bearer_token()
        headers = {"authorization": f"Bearer {token}"}
        info = []
        for album in albums_list:
            var = "{\"uri\":\"spotify:album:" + \
                album + "\",\"offset\":0,\"limit\":300}"
            querystring = {"operationName": "queryAlbumTracks", "variables": var,
                           "extensions": "{\"persistedQuery\":{\"sha256Hash\":\"f387592b8a1d259b833237a51ed9b23d7d8ac83da78c6f4be3e6a08edef83d5b\"}}"}
            raw_tracks = json.loads(requests.get(url_query, headers=headers, params=querystring).text)
            raw_tracks = raw_tracks["data"]["albumUnion"]["tracks"]["items"]
            info += [
                {"album_id": album,
                 "track_id": track["track"]["uri"].split(":")[2],
                 "name":track["track"]["name"],
                 "duration_ms":track["track"]["duration"]["totalMilliseconds"],
                 "artists":[el["profile"] for el in track["track"]["artists"]["items"]]} for track in raw_tracks
            ]

        return info

    def get_songs_stats(self, albums_list, token):
        url_query = "https://api-partner.spotify.com/pathfinder/v1/query"
        # token = self.get_bearer_token()
        headers = {"authorization": f"Bearer {token}"}
        info = []
        for album in albums_list:
            var = "{\"uri\":\"spotify:album:" + \
                album + "\",\"offset\":0,\"limit\":300}"
            querystring = {"operationName": "queryAlbumTracks", "variables": var,
                           "extensions": "{\"persistedQuery\":{\"sha256Hash\":\"f387592b8a1d259b833237a51ed9b23d7d8ac83da78c6f4be3e6a08edef83d5b\"}}"}
            raw_tracks = json.loads(requests.get(url_query, headers=headers, params=querystring).text)
            raw_tracks = raw_tracks["data"]["albumUnion"]["tracks"]["items"]
            info += [
                {"track_id": track["track"]["uri"].split(":")[2],
                 "playcount": int(track["track"]["playcount"]),
                 "date": dt.now().date()} for track in raw_tracks
            ]
        return info
