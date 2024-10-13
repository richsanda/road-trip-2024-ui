import os
import json
import sqlite3
from datetime import datetime

# Directory containing the JSON files
json_dir = '/Users/rich.s/experiences/road-trip-2024/receipts'

# SQLite database file
db_file = 'database.db'


# Function to create the table if it doesn't exist
def create_table(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                timestamp TEXT,
                timestamp_override TEXT,
                time TEXT,
                place TEXT,
                text TEXT,               
                record TEXT
            )
        ''')


# Function to insert a record into the table
def insert_record(conn, filename, timestamp, time, place, text, record):
    with conn:
        conn.execute('''
            INSERT INTO receipts (filename, timestamp, time, place, text, record)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            filename,
            timestamp if timestamp else None,
            time if time else None,
            place if place else None,
            text,
            json.dumps(record) if record else None
        ))


def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    # Create the table
    create_table(conn)

    # Iterate over JSON files in the directory
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(json_dir, filename)
            base_name = os.path.splitext(os.path.basename(filename))[0]
            with open(file_path, 'r') as file:
                data = json.load(file)
                timestamp = data.get('date', '')
                time = data.get('time', '')
                place = data.get('address', '')
                txt_path = os.path.join(json_dir, f"{base_name}.txt")
                text = None
                with open(txt_path, 'r') as txt_file:
                    text = txt_file.read()
                # Insert the record into the database
                insert_record(conn, base_name, timestamp, time, place, text, data)

    # Close the database connection
    conn.close()


if __name__ == '__main__':
    main()
