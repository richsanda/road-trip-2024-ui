import sqlite3
import json

# Connect to SQLite database
conn = sqlite3.connect('../../database.db')
cursor = conn.cursor()

# Query to get the necessary data
deletion = '''
SELECT pictures.id, notes.text, notes.id
FROM pictures
JOIN notes ON notes.type_id = pictures.id AND notes.type = 'picture';
'''

cursor.execute(deletion)
results = cursor.fetchall()

notes_to_remove = []


def build_json_data(note_text):

    # Check if text starts with "sign:"
    if note_text.startswith("sign:"):
        notes_to_remove.append(note_id)
        # Split the text into lines and handle accordingly
        lines = note_text.splitlines()
        sign_text = lines[0][len("sign:"):].strip()  # Get the text after "sign:" on the first line
        remaining_text = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""  # Join lines after the first as the note
        return {
            "sign": sign_text,  # Text after "sign:" on the first line
            "note": remaining_text  # Everything after the first line
        }

    # Check if text starts with "signs"
    if note_text.startswith("signs"):
        notes_to_remove.append(note_id)
        return {
            "signs": note_text[len("signs"):].strip()  # Trim "signs" and any leading/trailing whitespace
        }

    # Check if text starts with "caption"
    if note_text.startswith("caption"):
        notes_to_remove.append(note_id)
        return {
            "caption": note_text[len("caption"):].strip()  # Trim "signs" and any leading/trailing whitespace
        }

    # Check if the first line contains "miles" "temp" etc
    lines = note_text.splitlines()
    if lines and "miles" in lines[0]:
        miles_text = lines[0].strip()
        remaining_text = "\n".join(lines[1:]).strip()  # Combine the rest as the note, trimming whitespace
        notes_to_remove.append(note_id)
        return {
            "miles": miles_text,
            "note": remaining_text
        }

    if lines and "°" in lines[0]:
        temp_text = lines[0].strip()
        remaining_text = "\n".join(lines[1:]).strip()  # Combine the rest as the note, trimming whitespace
        notes_to_remove.append(note_id)
        return {
            "temp": temp_text,
            "note": remaining_text
        }

    if lines and "mpg" in lines[0]:
        mpg_text = lines[0].strip()
        remaining_text = "\n".join(lines[1:]).strip()  # Combine the rest as the note, trimming whitespace
        notes_to_remove.append(note_id)
        return {
            "mpg": mpg_text,
            "note": remaining_text
        }

    # Default case: no "signs" or "miles" condition met
    return {
        "note": note_text.strip()
    }


# Iterate over results, build JSON, and update the pictures.data column
for picture_id, note_text, note_id in results:
    # Generate JSON data based on note_text
    json_data = build_json_data(note_text)

    # Convert JSON to a string for storage
    json_string = json.dumps(json_data)

    # Update the pictures table with the JSON data
    update_query = '''
    UPDATE pictures
    SET data = ?
    WHERE id = ?;
    '''
    cursor.execute(update_query, (json_string, picture_id))

# Execute the DELETE query with the list of IDs
deletion = "DELETE FROM notes WHERE id IN ({})".format(",".join("?" for _ in notes_to_remove))
cursor.execute(deletion, notes_to_remove)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("JSON data has been inserted into pictures.data.")

print(f"{len(notes_to_remove)} notes to remove still...")