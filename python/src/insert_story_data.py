import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('database.db')  # Using your DB name 'database.db'
cursor = conn.cursor()

# Create the 'stories' table with the new structure
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        category TEXT NOT NULL,
        date TEXT,   -- Leave date blank for now
        time TEXT,   -- Leave time blank for now
        sydney_rank INTEGER,
        dada_rank INTEGER
    )
''')

# Load JSON data from file
with open('top-10.json', 'r') as f:
    data = json.load(f)

# Insert each entry into the 'stories' table
for entry in data:
    text = entry.get("text")
    category = entry.get("category")
    sydney_rank = None  # Leaving as None for now, change this as needed
    dada_rank = None    # Leaving as None for now, change this as needed

    cursor.execute('''
        INSERT INTO stories (text, category, date, time, sydney_rank, dada_rank)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (text, category, None, None, sydney_rank, dada_rank))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully into the 'stories' table!")
