import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('../database.db')
cursor = conn.cursor()

# Load the playlist_info from a JSON file
with open('road-trip-songs.june-10-2024.json', 'r') as file:
    playlist_info = json.load(file)

# Iterate over the tracks in the playlist and apply insert/update logic
for track in playlist_info['tracks']:
    # Check if the track already exists by song_link
    cursor.execute("SELECT id FROM songs WHERE song_link = ?", (track['song_link'],))
    existing_row = cursor.fetchone()

    if existing_row:
        # Update existing record: add spotify_id, added_at, and playlist fields only
        cursor.execute('''
            UPDATE songs 
            SET 
                spotify_id = ?, 
                added_at = ?, 
                playlist_id = ?, 
                playlist_name = ?, 
                playlist_owner = ? 
            WHERE id = ?
        ''', (
            track['id'],  # spotify_id
            track['added_at'],  # added_at
            playlist_info['id'],  # playlist_id
            playlist_info['name'],  # playlist_name
            playlist_info['owner'],  # playlist_owner
            existing_row[0]  # id from existing_row
        ))
    else:
        # Insert new record with all fields (id auto-increments, ordinal is NULL if not provided)
        cursor.execute('''
            INSERT INTO songs 
            (spotify_id, song_link, artist_name, song_name, image_link, added_at, 
             playlist_id, playlist_name, playlist_owner, ordinal)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            track['id'],  # spotify_id
            track['song_link'],  # song_link
            track['artist_name'],  # artist_name
            track['song_name'],  # song_name
            track['image_link'],  # image_link
            track['added_at'],  # added_at
            playlist_info['id'],  # playlist_id
            playlist_info['name'],  # playlist_name
            playlist_info['owner'],  # playlist_owner
            track.get('ordinal', None)  # ordinal (use None if not provided)
        ))

# Commit the transaction and close the connection
conn.commit()
conn.close()
