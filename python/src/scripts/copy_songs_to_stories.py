import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('../../database.db')
cursor = conn.cursor()

# Step 1: Retrieve all rows from the songs table
cursor.execute("SELECT * FROM songs")
rows = cursor.fetchall()

# Step 2: Get column names from songs table for JSON keys
column_names = [description[0] for description in cursor.description]

# Step 3: Insert each song into the stories table
for row in rows:
    # Create the text for each song in the desired format
    song_name = row[column_names.index('song_name')].lower()
    artist_name = row[column_names.index('artist_name')].lower()
    text = f"{song_name} -- {artist_name}"

    # Convert the row to a dictionary for JSON storage
    song_data = dict(zip(column_names, row))
    song_json_blob = json.dumps(song_data, indent=4)

    # Insert into the stories table
    cursor.execute("""
        INSERT INTO stories (text, category, data)
        VALUES (?, ?, ?)
    """, (text, 'songs', song_json_blob))

# Commit and close the connection
conn.commit()
conn.close()

print("Each song has been successfully stored as a separate row in the stories table.")
