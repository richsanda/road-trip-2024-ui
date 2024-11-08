import requests
import json

# Your access token
access_token = 'BQB3xKUfxk_nIu623JUYvbJ2_5LUIfkYwzkEHdUQTuwoGw4-Fy1sO8xOnu_wO7epEwMxftv43BwlA0U_I7aNpASlJ2fW7S2bvFqa5Yc61ezE5sg9Tw4'
# Your playlist ID
playlist_id = '5tsTWtzNU7OO2wEG2GbTmO'

# Set the URL and headers
url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Retrieve the playlist
response = requests.get(url, headers=headers)
playlist_data = response.json()

# Create the root object to hold all playlist information
playlist_info = {
    "id": playlist_data['id'],                                  # Spotify ID for the playlist
    "name": playlist_data['name'],                              # Playlist name
    "description": playlist_data.get('description', ''),        # Playlist description, if available
    "owner": playlist_data['owner']['display_name'],            # Creator's display name
    "snapshot_id": playlist_data['snapshot_id'],                # Can approximate the creation time
    "tracks": []                                                # This will hold individual track data
}

# Use the first track's added_at date as an approximation for the playlist creation date
if playlist_data['tracks']['items']:
    playlist_info["approx_created_at"] = playlist_data['tracks']['items'][0]['added_at']

# Iterate through the tracks and collect the required data for each
for item in playlist_data['tracks']['items']:
    track = item['track']
    track_info = {
        "id": track['id'],                                     # Spotify ID for the track
        "artist_name": track['artists'][0]['name'],
        "song_name": track['name'],
        "image_link": track['album']['images'][0]['url'],      # Get the first image
        "song_link": track['external_urls']['spotify'],        # Spotify link
        "added_at": item['added_at']                           # Date the song was added
    }
    playlist_info["tracks"].append(track_info)                 # Add track info to the "tracks" list in the root object

# Print the formatted JSON output
print(json.dumps(playlist_info, indent=4))
