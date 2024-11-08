import os
import shutil
from connection import get_db_connection

# Database and query setup
query = """
select t.filename from timeline as t 
join timeline_notes as tn on tn.type = t.type and tn.type_id = t.type_id 
where tn.keep = 1 and tn.type='picture';
  """

# Directories setup
source_dir = '/Users/rich.s/Documents/phone-2024-07-31/DCIM/Camera/'  # Directory where your .jpg files are located
destination_dir = '/Users/rich.s/whateva/road-trip-2024-ui/images/pictures/'  # Directory where you want to copy the files

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Connect to the database
conn = get_db_connection('../database.db')
cursor = conn.cursor()

# Execute the query
cursor.execute(query)
base_filenames = cursor.fetchall()

# Iterate through the base filenames and copy the files
for (base_filename,) in base_filenames:
    source_file = os.path.join(source_dir, f"{base_filename}.jpg")
    destination_file = os.path.join(destination_dir, f"{base_filename}.jpg")

    if os.path.exists(source_file):
        shutil.copy(source_file, destination_file)
        print(f"Copied {source_file} to {destination_file}")
    else:
        print(f"File {source_file} not found!")

# Close the database connection
conn.close()
