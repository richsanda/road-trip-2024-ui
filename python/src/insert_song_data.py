import sqlite3
import json

# Connect to (or create) a SQLite3 database
conn = sqlite3.connect('../database.db')
cursor = conn.cursor()

# Create the 'messages' table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY,
artist_name TEXT,
song_name INTEGER,
image_link TEXT,
song_link TEXT,
ordinal INTEGER
)
''')

# Open and read the CSV file
with open('road-trip-songs.json', 'r') as file:
    data = json.load(file)

i = 0
# Insert each row into the 'songs' table
for entry in data:
    i += 1
    cursor.execute('''
        INSERT INTO songs (artist_name, song_name, image_link, song_link, ordinal)
        VALUES (?, ?, ?, ?, ?)
        ''', (entry['artist_name'], entry['song_name'], entry['image_link'], entry['song_link'], i))

# Commit and close the connection
conn.commit()
conn.close()
