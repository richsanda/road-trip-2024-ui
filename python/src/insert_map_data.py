import os
import json
import sqlite3

# Directory containing the JSON files
json_dir = '/Users/rich.s/experiences/road-trip-2024/maps'

# SQLite database file
db_file = 'database.db'


# Function to create the table if it doesn't exist
def create_table(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS maps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                filename TEXT,                
                start_time TEXT,
                end_time TEXT,
                start_place TEXT,
                end_place TEXT,
                map_places TEXT,
                record TEXT
            )
        ''')


# Function to insert a record into the table
def insert_record(conn, filename, start_time, end_time, start_place, end_place, map_places, record):
    with conn:
        conn.execute('''
            INSERT INTO maps (filename, start_time, end_time, start_place, end_place, map_places, record)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            filename,
            start_time if start_time else None,
            end_time if end_time else None,
            start_place if start_place else None,
            end_place if end_place else None,
            json.dumps(map_places) if map_places else None,
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
                start_time = data.get('start_time', '')
                end_time = data.get('end_time', '')
                start_place = data.get('start_place', '')
                end_place = data.get('end_place', '')
                map_places = data.get('map_places', [])
                # Insert the record into the database
                insert_record(conn, base_name, start_time, end_time, start_place, end_place, map_places, data)

    # Close the database connection
    conn.close()


if __name__ == '__main__':
    main()
