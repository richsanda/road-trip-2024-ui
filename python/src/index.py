import sqlite3
from datetime import datetime, timedelta
import json

# Connect to (or create) a SQLite3 database
conn = sqlite3.connect('database.db')

timezone_adjustments = [
    {
        "timestamp": "2024-07-01T20:05:00",
        "timezone": -1
    },
    {
        "timestamp": "2024-07-02T21:00:00",
        "timezone": -2
    },
    {
        "timestamp": "2024-07-11T18:50:00",
        "timezone": -1
    },
    {
        "timestamp": "2024-07-13T15:45:00",
        "timezone": 0
    }
]


def adjust_for_time_zone(timestamp, adjustments=None):
    timezone_offset = 0

    adjustments = adjustments or timezone_adjustments

    # Handle timestamps with or without fractional seconds
    def parse_timestamp(ts):
        # Handle timestamps with missing seconds by appending ":00"
        if len(ts) == 16:  # "YYYY-MM-DDTHH:MM" is 16 characters long
            ts += ":00"
        try:
            return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")

    # Convert the input timestamp string to a datetime object
    input_time = parse_timestamp(timestamp)

    # Sort the adjustments by timestamp to ensure they are in chronological order
    adjustments.sort(key=lambda x: x['timestamp'])

    # Find the latest timezone adjustment that applies to the input timestamp
    for adjustment in adjustments:
        adjustment_time = parse_timestamp(adjustment['timestamp'])

        # Apply the adjustment if the adjustment_time is less than or equal to the input_time
        if input_time >= adjustment_time:
            timezone_offset = adjustment['timezone']
        else:
            break

    # Adjust the input timestamp by the timezone offset in hours
    adjusted_time = input_time + timedelta(hours=timezone_offset)

    return adjusted_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] if '.' in timestamp else adjusted_time.strftime(
        "%Y-%m-%dT%H:%M:%S")


def add_hours_to_iso_timestamp(timestamp_str, hours):
    # Parse the input string using fromisoformat to handle fractional seconds
    timestamp = datetime.fromisoformat(timestamp_str)

    # Add the specified number of hours
    updated_timestamp = timestamp + timedelta(hours=hours)

    # Convert the updated datetime back to an ISO string, preserving microseconds if present
    return updated_timestamp.isoformat()


maps_query = '''
SELECT id, timestamp, start_time, end_time, start_place_json, end_place_json, filename
FROM maps
WHERE end_time IS NOT NULL
AND hide = 0
ORDER BY 
    CASE 
        WHEN timestamp IS NULL THEN 1 
        ELSE 0 
    END, 
    timestamp ASC, 
    start_time ASC,
    end_time ASC;
'''

messages_query = '''
SELECT id, sender_name, timestamp_ms, content
FROM messages;
'''

shazams_query = '''
SELECT id, date, time, title, artist, link, about_track
FROM shazams
ORDER BY 
    date ASC, 
    time ASC;
'''

receipts_query = """
SELECT id, timestamp, time, place, filename, place_json
FROM receipts
ORDER BY 
    timestamp ASC, 
    time ASC;
"""

pictures_query = """
SELECT id, timestamp, filename, address, address_json
FROM pictures
"""

stories_query = """
SELECT id, date, time, category, text
FROM stories
ORDER BY 
    date ASC, 
    time ASC;
"""


def fetch(query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# for record in fetch(messages_query):
#     type_id = record[0]
#     description = f"{record[1]}: {record[3]}"
#     offset = -4 * 3600
#     timestamp = datetime.utcfromtimestamp(record[2] / 1000 + offset).isoformat()
#     timestamp = adjust_for_time_zone(timestamp)
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO timeline (timestamp, description, type, type_id)
#         VALUES (?, ?, ?, ?)
#         ''', (timestamp, description, 'message', type_id))


def migrate_data(messages):
    # Sort messages by the timestamp (index 2), assuming timestamps are in milliseconds
    messages.sort(key=lambda record: record[2])

    grouped_messages = []
    current_group = []
    time_threshold = timedelta(hours=0.5)
    contains_rich = False

    for record in messages:
        type_id = record[0]
        sender_name = record[1]
        message_content = record[3]
        offset = -4 * 3600
        timestamp = datetime.utcfromtimestamp(record[2] / 1000 + offset)
        group_timestamp = None

        timestamp_str = timestamp.isoformat()
        adjusted_timestamp_str = adjust_for_time_zone(timestamp_str)
        timestamp = datetime.fromisoformat(adjusted_timestamp_str)

        # Replace sender names
        if sender_name == 'Rich Sanda':
            sender_name = 'rich'
        elif sender_name == 'Laura McCarthy Sanda':
            sender_name = 'laura'

        # Check if group is complete (one-hour gap + contains 'rich')
        if current_group:
            last_timestamp = current_group[-1]['timestamp']
            if timestamp - last_timestamp > time_threshold and contains_rich:
                # Append the group if it meets the criteria
                grouped_messages.append(current_group)
                current_group = []
                contains_rich = False  # Reset for the next group

        # Add current message to the group
        current_group.append({
            'type_id': type_id,
            'timestamp': timestamp,
            'sender_name': sender_name,
            'message': message_content
        })

        # Check if this message is from 'rich'
        if sender_name == 'rich':
            contains_rich = True

    # Add the last group if it meets the criteria
    if current_group and contains_rich:
        grouped_messages.append(current_group)

    insert_grouped_messages(grouped_messages)


def insert_grouped_messages(grouped_messages):
    cursor = conn.cursor()

    for group in grouped_messages:
        # Use the last message's timestamp and type_id for the group
        first_rich_message = next((message for message in group if message['sender_name'] == 'rich'), None)
        group_timestamp = first_rich_message['timestamp'].isoformat()
        group_type_id = first_rich_message['type_id']

        # Create a JSON array of objects with each message's details
        json_messages = json.dumps([
            {
                'timestamp': msg['timestamp'].isoformat(),
                'sender_name': msg['sender_name'],
                'message': msg['message']
            }
            for msg in group
        ])

        # Insert the grouped entry into the timeline table
        cursor.execute('''
            INSERT INTO timeline (timestamp, description, type, type_id)
            VALUES (?, ?, ?, ?)
        ''', (group_timestamp, json_messages, 'message', group_type_id))

    conn.commit()


cursor = conn.cursor()
migrate_data(cursor.execute(messages_query).fetchall())


def get_end_timestamp(date, start_time, end_time):
    # Combine date with start_time and end_time
    start_datetime_str = f"{date}T{start_time}"
    end_datetime_str = f"{date}T{end_time}"

    # Parse start and end times as datetime objects
    try:
        start_datetime = datetime.fromisoformat(start_datetime_str)
        end_datetime = datetime.fromisoformat(end_datetime_str)

        # If end_time is earlier than start_time, it means the event ends the next day
        if end_datetime < start_datetime:
            # Increment the date by one day
            end_datetime += timedelta(days=1)

        # Return the end timestamp as an ISO formatted string
        return end_datetime.isoformat()
    except:
        return None


# SELECT id, timestamp, start_time, end_time, start_place, end_place
for record in fetch(maps_query):
    type_id = record[0]
    date = record[1]
    start_time = record[2]
    end_time = record[3]
    start_place_json = record[4]
    end_place_json = record[5]
    filename = record[6]
    timestamp = f"{record[1]}T{record[2]}"
    end_timestamp = get_end_timestamp(date, start_time, end_time)
    timestamp = adjust_for_time_zone(timestamp)
    end_timestamp = adjust_for_time_zone(end_timestamp) if end_timestamp else None

    description_json = {
        "timestamp": timestamp,
        "end_timestamp": end_timestamp,
        "place": json.loads(start_place_json) if start_place_json else {},  # Rename start_place_json to "place"
        "end_place": json.loads(end_place_json) if end_place_json else {} # Rename end_place_json to "end_place"
    }

    description = json.dumps(description_json)

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO timeline (timestamp, description, filename, type, type_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, description, filename, 'map', type_id))

# SELECT id, date, time, title, artist, link
for record in fetch(shazams_query):
    type_id = record[0]
    title = record[3]
    artist = record[4]
    link = record[5]
    about_track = record[6]
    timestamp = f"{record[1]}T{record[2]}"
    timestamp = adjust_for_time_zone(timestamp)

    # Parse the image_url JSON string
    image_data = json.loads(about_track) if about_track else {}

    # Extract the coverart URL if it exists
    coverart_url = image_data.get('images', {}).get('coverart', None)

    # Create a JSON-formatted string with title, artist, and link
    description_json = json.dumps({
        "title": title,
        "artist": artist,
        "link": link,
        "image_url": coverart_url
    })

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO timeline (timestamp, description, filename, type, type_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, description_json, coverart_url, 'shazam', type_id))


# SELECT id, timestamp, time, place, record
for record in fetch(receipts_query):
    type_id = record[0]
    place = record[3]
    timestamp = f"{record[1]}T{record[2]}"
    filename = record[4]
    place_json = record[5]
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO timeline (timestamp, place, description, filename, type, type_id)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, place, place_json, filename, 'receipt', type_id))

# SELECT id, timestamp, address
for record in fetch(pictures_query):
    type_id = record[0]
    timestamp = record[1]
    filename = record[2]
    place = record[3]
    description = record[4]
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO timeline (timestamp, filename, description, place, type, type_id)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, filename, description, place, 'picture', type_id))

# for record in fetch(stories_query):
#     type_id = record[0]
#     date = record[1]
#     time = record[2]
#     category = record[3]
#     text = record[4]
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO timeline (timestamp, description, type, type_id)
#         VALUES (?, ?, ?, ?)
#         ''', (f"{date}T{time}", f"{category}: {text}", 'story', type_id))

# Commit and close the connection
conn.commit()
conn.close()
