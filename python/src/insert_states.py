import sqlite3

# Connect to SQLite3 database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# List of states/provinces to be added to the 'category' column
states = [
    'massachusetts', 'new york', 'pennsylvania', 'ohio', 'michigan', 'wisconsin',
    'minnesota', 'north dakota', 'montana', 'saskatchewan', 'alberta',
    'wyoming', 'south dakota', 'iowa', 'illinois', 'indiana', 'ontario'
]

# Insert each state/province into the stories table with the 'category' column set
for state in states:
    cursor.execute('''
    INSERT INTO stories (text, category) VALUES (?, 'state')
    ''', (state,))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("States and provinces successfully inserted into the category column.")
