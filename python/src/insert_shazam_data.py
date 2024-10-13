import sqlite3
import csv

# Connect to (or create) a SQLite3 database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the 'shazams' table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS shazams (
    id INTEGER PRIMARY KEY,
    key INTEGER,
    date TEXT,
    time TEXT,
    title TEXT,
    artist TEXT,
    link TEXT,
    track_key INTEGER
)
''')

# Open and read the CSV file
with open('/Users/rich.s/experiences/road-trip-2024/shazam-songs.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    # Skip header if exists
    next(csvreader)

    # Insert each row into the 'shazams' table
    for row in csvreader:
        cursor.execute('''
        INSERT INTO shazams (key, date, time, title, artist, link, track_key)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', row)

# Commit and close the connection
conn.commit()
conn.close()
