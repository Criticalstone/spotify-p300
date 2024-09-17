# Run this command in your terminal
# pip install spotipy BeutifulSoup4 requests

import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

URL = 'https://sverigesradio.se/avsnitt/p300-hela-listan'
response = requests.get(URL)
html_content = response.content

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')
song_elements = soup.select('div.publication-text.text-editor-content p a')

print(len(song_elements))
for song in song_elements:
    print(song.text)

# Setup the Spotify API
# Login here to get your credentials https://developer.spotify.com/dashboard
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='CLIENT_ID',
    client_secret='CLIENT_SECRET',
    redirect_uri='http://localhost:8080',
    scope='playlist-modify-private'
))

# Define the playlist id
PLAYLIST_ID = 'PLAYLIST_ID'
track_ids = []

# Delete any current items in the playlist
currentItems = sp.playlist_items(PLAYLIST_ID)
for item in currentItems['items']:
    print("deleting ", item['track']['name'])
    track = item['track']
    sp.playlist_remove_all_occurrences_of_items(PLAYLIST_ID, [track['id']])

# Search for songs that match the names from the website
for song in song_elements:
    res = sp.search(q=song.text, limit=1, type='track')
    if res['tracks']['items']:
        track_id = res['tracks']['items'][0]['id']
        track_ids.append(track_id)
    else:
        print(f"Track not found: {song.text}")

print(len(track_ids))

# Add tracks to the playlist
# Not sure how many tracks can be added at once, so I'm adding 10 at a time.
# It definitely does not handle hundreds at once...
x = 0
for i in range(len(track_ids)//10 + 1):
    sp.playlist_add_items(PLAYLIST_ID, track_ids[i*10:i*10+10])
    x += 10

print(x)
print("Tracks added to the playlist successfully!")
