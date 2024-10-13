import sqlite3
import json

# Connect to (or create) a SQLite3 database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the 'messages' table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    sender_name TEXT,
    timestamp_ms INTEGER,
    timestamp TEXT,
    content TEXT
)
''')

# Open and read the JSON file with UTF-8 encoding
with open('/Users/rich.s/experiences/road-trip-2024/laura-messenger.json', 'r', encoding='latin1') as file:

    data = json.load(file)

    for entry in data['messages']:
        content = entry.get('content', None)
        if content:
            print(content)
            encoded_string = "\u00e2\u009d\u00a4\u00ef\u00b8\u008f"

            # First, encode it using Latin-1
            decoded_bytes = encoded_string.encode('latin1')

            # Then decode it back using UTF-8
            final_string = decoded_bytes.decode('utf-8')

            print(final_string)
            # If content has escaped unicode sequences, decode them
            content = content.encode('latin1').decode('utf-8')

            cursor.execute('''
                INSERT INTO messages (sender_name, timestamp_ms, content)
                VALUES (?, ?, ?)
            ''', (entry['sender_name'], entry['timestamp_ms'], content))


# Commit and close the connection
conn.commit()
conn.close()
