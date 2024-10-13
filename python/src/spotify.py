import json

# Load the original JSON file
with open('/Users/rich.s/experiences/road-trip-2024-tracks-4.json', 'r') as file:
    data = json.load(file)

# Simplify the JSON to only include artist name, song name, image link, and song link
simplified_data = []

i = 0
for item in data['items']:
    track_info = {
        'artist_name': item['artists'][0]['name'],
        'song_name': item['name'],
        'image_link': item['album']['images'][0]['url'],
        'song_link': item['external_urls']['spotify']
    }
    simplified_data.append(track_info)
    i += 1
    print(f"{i}. {track_info['song_name']} -- {track_info['artist_name']}")

# Save the simplified JSON to a new file
with open('simplified_spotify_recent_tracks.json', 'w') as file:
    json.dump(simplified_data, file, indent=4)

print("Simplified JSON has been saved as 'simplified_spotify_recent_tracks.json'")
