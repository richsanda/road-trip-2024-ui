import os
import json
import sqlite3
from datetime import datetime

# Directory containing the JSON files
json_dir = '/Users/rich.s/experiences/road-trip-2024/pictures'

# SQLite database file
db_file = 'database.db'

# Function to create the table if it doesn't exist
def create_table(conn):
    with conn:
        conn.execute('DROP TABLE IF EXISTS pictures')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS pictures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                filename TEXT,
                address TEXT
            )
        ''')


# Function to insert a record into the table
def insert_record(conn, timestamp, filename, address):
    with conn:
        conn.execute('''
            INSERT INTO pictures (timestamp, filename, address)
            VALUES (?, ?, ?)
        ''', (convert_to_iso_format(timestamp), filename, address))


def convert_to_iso_format(timestamp):
    # Define the original format
    original_format = "%Y:%m:%d %H:%M:%S"

    # Parse the original timestamp
    dt = datetime.strptime(timestamp, original_format)

    # Convert to ISO 8601 format
    return dt.isoformat()


def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    # Create the table
    create_table(conn)

    # Iterate over JSON files in the directory
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(json_dir, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                timestamp = data.get('Timestamp', '')
                base_name = os.path.splitext(os.path.basename(filename))[0]
                address = data.get('Address', '')
                # Insert the record into the database
                insert_record(conn, timestamp, base_name, address)

    # Close the database connection
    conn.close()


if __name__ == '__main__':
    main()
