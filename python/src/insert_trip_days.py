import json
import sqlite3

# Connect to SQLite3 database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Load the JSON array from a file
with open('trip-days.json', 'r') as file:
    data = json.load(file)

# Insert each item in the JSON array into the stories table
for item in data:
    label = item.get('label')
    value = item.get('value')

    cursor.execute('''
    INSERT INTO stories (text, time, category) VALUES (?, ?, 'day')
    ''', (label, value))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data successfully inserted into the stories table.")
