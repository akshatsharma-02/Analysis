import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import mysql.connector

# Spotify API credentials
client_id="350c529fb1b942de9cd12ce3620bc92e"
client_secret="7471acabef4a41fdaeb880c952ce9576"

# Initialize Spotipy client with credentials
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

conn=mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="playlist_analysis"
    )
cursor=conn.cursor()

# Retrieve playlist information
playlist_results = sp.search(q='pov:you are in love', type='playlist')

for playlist in playlist_results['playlists']['items']:
    playlist_id = playlist['id']
    playlist_name = playlist['name']
    playlist_owner = playlist['owner']['display_name']
    playlist_description = playlist['description']
    playlist_image_url = playlist['images'][0]['url'] if playlist['images'] else None
    playlist_track_count = playlist['tracks']['total']

# Print playlist information
"""print("Playlist Name:", playlist_name)
print("Playlist Owner:", playlist_owner)
print("Playlist Description:", playlist_description)
print("Playlist Image URL:", playlist_image_url)
print("Number of Tracks:", playlist_track_count)"""

# Retrieve tracks in the playlist
track_result = sp.playlist_tracks(playlist_id)

# Iterate over tracks
for idx, item in enumerate(track_result['items']):
    track = item['track']
    track_id = track['id']
    track_name = track['name']
    track_artists = ", ".join([artist['name'] for artist in track['artists']])
    track_album = track['album']['name']
    track_release_date = track['album']['release_date']
    track_popularity = track['popularity']
    track_duration_ms = track['duration_ms']
    track_duration_min = str(round(track['duration_ms']/60000,0))
    track_duration_sec = str(round((track['duration_ms']/1000)%60,0))
    track_duration = track_duration_min+"mins"+track_duration_sec+"secs"  
    track_url = track['external_urls']['spotify']

    audio_feature= sp.audio_features([track_id])
    features= audio_feature[0]
    track_danceability= features.get('danceability')
    track_energy= features.get('energy')
    track_loudness= features.get('loudness')
    track_speechiness= features.get('speechiness')
    track_acousticness= features.get('acousticness')

    song_table="INSERT INTO song(Track id,Track name,Track Artists,Track Album, Release Date, Popularity Score,Duration,Danceability,Energy,Loudness,Speechiness, Acousticness,Spotify URL) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    song_data=(track_id,track_name,track_artists,track_album,track_release_date,track_popularity,track_duration,track_danceability,track_energy,track_loudness,track_speechiness,track_acousticness,track_url)
    cursor.execute(song_table,song_data)
    conn.commit()

    # Print track information
    """print(f"\nTrack {idx+1}:")
    print("Track Name:", track_name)
    print("Artists:", track_artists)
    print("Album:", track_album)
    print("Release Date:", track_release_date)
    print("Popularity Score:", track_popularity)
    print("Duration:", track_duration_min,"min ",track_duration_sec,"sec")
    print("Danceability:", track_danceability)
    print("Energy:", track_energy)
    print("Loudness:", track_loudness)
    print("Speechiness:", track_speechiness)
    print("Acousticness:", track_acousticness)
    print("Spotify URL:", track_url)"""


"""select_query="select * from song_table"
cursor.execute(select_query)
rows= cursor.fetchall()

for row in rows:
    print(row)"""

cursor.close()
conn.close()