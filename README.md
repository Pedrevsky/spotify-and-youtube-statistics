# Spotify and Youtube stats

Working with Spotify and Youtube APIs to collect statistics from channels, artists, etc.

I want to see if there is any correlation between Spotify play count and youtube view count of the same songs

For today I have ready getting data scripts with classes:
- SpotifyAPI
- YoutubeAPI
- Database

----------------------------------

### SpotifyAPI:
I don't use public Spotify API because it doesn't provide the information that I want.

Instead, I managed to discover a way to get data from the website. In the desktop version of Spotify, you can see (almost) every song play count but in the web application this information is hidden and you can see only the top 10 songs play count within an artist. 

But info in album view is only hidden in Frontend, if u check the network tab in inspect tool you can find data that is still there ([check this video](https://www.youtube.com/watch?v=h18NhHBQFu8))

Using [Insomnia](https://insomnia.rest/download) I managed to write requests for all info that I want. The last obstacle was the bearer token which was needed for authorization. I discovered that it is written on the Spotify source page inside one of the script tags. This token is valid only if you get it after logging into your account so I wrote code that logins to my account and then get the token.

My SpotifyAPI class has 5 methods:
- get_bearer_token
- get_artists
- get_albums_info
- get_songs_info
- get_songs_stats

-----------------

### YoutubeAPI

Working with Youtube API was much easier, there was all I want in public API which is well documented [here](https://developers.google.com/youtube/v3?hl=en)

I wrote YoutubeAPI class that has 4 methods:
- get_channels_info
- get_channels_stats
- get_videos_info
- get_videos_stats



------------------

### Database

My Database class has methods for creating tables if they don't exist, inserting data, checking if data exists, and appending data (if it's necessary). I use PostgreSQL database engine

-----------------

##### In the future:
- add errors handling
- add logging
- maybe change database to NoSQL
- analyze time series data
