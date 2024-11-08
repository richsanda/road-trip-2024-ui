import os
import json
import sqlite3

# Set your directory and database file
directory = "/Users/rich.s/experiences/road-trip-2024/maps-images/"
database_file = '../../database.db'  # Replace with your database file name


# Connect to the SQLite database
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Iterate over all JSON files in the specified directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        # Create the full path to the file
        file_path = os.path.join(directory, filename)

        # Open and read the JSON file
        with open(file_path, 'r') as json_file:
            file_contents = json_file.read()

        # Remove the .json suffix from the filename
        base_filename = filename[:-5]  # Removes the last 5 characters ('.json')

        # Prepare and execute the SQL update command
        cursor.execute("UPDATE maps SET record = ? WHERE filename = ?", (file_contents, base_filename))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("All JSON files have been used to update the database.")