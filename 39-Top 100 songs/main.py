import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET = os.getenv("SPOTIFY_SECRET")
REDIRECT_URI = "http://example.com"

URL = "https://www.billboard.com/charts/hot-100/"

user_input = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = user_input.split("-")[0] 

response = requests.get(f"{URL}{user_input}/")
response.raise_for_status()
billboard_web_page = response.text

soup = BeautifulSoup(billboard_web_page, "html.parser")

all_songs = soup.select("li ul li h3")
song_titles = [song.getText().strip() for song in all_songs]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                            cache_path="token.txt"))

user_id = sp.current_user()["id"]

playlist_name = f"{user_input} Billboard 100"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
playlist_id = playlist["id"]
print(f"Created playlist: {playlist_name} with ID: {playlist_id}")

song_uris = []

for title in song_titles:
    try:
        result = sp.search(q=f"track:{title} year:{year}", type="track", limit=1)
        track = result['tracks']['items'][0]
        song_uris.append(track['uri'])
        pprint(f"Found: {title} - {track['uri']}")
    except IndexError:
        pprint(f"Could not find {title} on Spotify. Skipping...")


if song_uris:
    sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
    print(f"Added {len(song_uris)} songs to the playlist {playlist_name}.")
else:
    print("No songs were added to the playlist.")