from datetime import datetime, timedelta
from connection import get_db_connection
import json

# Connect to (or create) a SQLite3 database
conn = get_db_connection()

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
        "timestamp": "2024-07-05T17:00:00",
        "timezone": 0
    },
    {
        "timestamp": "2024-07-07T10:00:00",
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


def adjust_to_local_time_from_z(timestamp_z, hours):

    if not timestamp_z:
        return None

    # Parse the UTC timestamp
    utc_time = datetime.strptime(timestamp_z, "%Y-%m-%dT%H:%M:%SZ")

    # Subtract 4 hours to adjust to local time
    adjusted_time = utc_time - timedelta(hours=hours)

    # Return the adjusted time in ISO 8601 format
    return adjusted_time.isoformat()


def convert_to_12_hour_format(time_str):
    """Converts 24-hour format (e.g., '14:30') to 12-hour format with 'a'/'p'."""
    if not time_str or ':' not in time_str or time_str == "N/A":
        return None  # Return None if the input is not a valid time string

    try:
        hour, minute = map(int, time_str.split(':'))
        period = "a" if hour < 12 else "p"

        # Convert hour to 12-hour format
        hour = hour if hour == 12 or hour == 0 else hour % 12
        hour = 12 if hour == 0 else hour  # Handle midnight as 12am

        return f"{hour}:{minute:02d}{period}"
    except ValueError:
        return None  # In case the time string isn't properly formatted



def transform_map_info(record):
    # Extract fields
    duration_hours = record.get("duration_hours", 0)
    duration_minutes = record.get("duration_minutes", 0)
    distance = record.get("distance", "0")
    units = record.get("units", "mi")
    start_time = record.get("start_time", "")
    end_time = record.get("end_time", "")
    place = record.get("place", "")
    start_place = record.get("start_place", "")
    end_place = record.get("end_place", "")
    nearby_places = record.get("nearby_places", [])

    # Format duration as "X hours, Y minutes"
    if duration_hours > 0:
        duration = f"{duration_hours} hour{'s' if duration_hours > 1 else ''}, {duration_minutes} minute{'s' if duration_minutes != 1 else ''}"
    else:
        duration = f"{duration_minutes} minute{'s' if duration_minutes != 1 else ''}"

    # Format distance as "X units"
    distance_str = f"{distance} {units}"

    # Convert start and end times to 12-hour format, handle case where one is missing
    start_time_12hr = convert_to_12_hour_format(start_time)
    end_time_12hr = convert_to_12_hour_format(end_time)

    # Format time range (use arrow only if both times are available)
    if start_time_12hr and end_time_12hr:
        when = f"{start_time_12hr} -> {end_time_12hr}"
    elif start_time_12hr:
        when = start_time_12hr
    elif end_time_12hr:
        when = end_time_12hr
    else:
        when = None

    if place and not start_place:
        start_place = place

    # Format places (use arrow only if both places are available)
    if start_place and end_place:
        where = f"{start_place} -> {end_place}"
    elif start_place:
        where = start_place
    elif end_place:
        where = end_place
    else:
        where = None

    # Create the final simplified object
    transformed = {
        "duration": duration,
        "distance": distance_str,
        # "when": when,
        "location": where,
        "nearby": nearby_places
    }

    # Filter out any fields that are None
    return {k: v for k, v in transformed.items() if v is not None}


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
SELECT id, timestamp, start_time, end_time, start_place_json, end_place_json, filename, record
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
SELECT id, timestamp, time, place, filename, place_json, record
FROM receipts
ORDER BY 
    timestamp ASC, 
    time ASC;
"""

pictures_query = """
SELECT id, timestamp, filename, address, address_json, data
FROM pictures 
"""

stories_query = """
SELECT id, date, time, category, text, dada_rank, sydney_rank, data
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

    # insert_grouped_messages(grouped_messages)


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
            INSERT INTO timeline (timestamp, data, type, type_id)
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
    info_json = record[7]
    timestamp = f"{record[1]}T{record[2]}"
    end_timestamp = get_end_timestamp(date, start_time, end_time)
    timestamp = adjust_for_time_zone(timestamp)
    end_timestamp = adjust_for_time_zone(end_timestamp) if end_timestamp else None

    info = transform_map_info(json.loads(info_json))

    data_json = {
        "timestamp": timestamp,
        "end_timestamp": end_timestamp,
        "place": json.loads(start_place_json) if start_place_json else None,  # Rename start_place_json to "place"
        "end_place": json.loads(end_place_json) if end_place_json else None,  # Rename end_place_json to "end_place"
        "info": info
    }

    data = json.dumps(data_json)

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO timeline (timestamp, data, filename, type, type_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, data, filename, 'map', type_id))

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
    data_json = json.dumps({
        "title": title,
        "artist": artist,
        "link": link,
        "image_url": coverart_url
    })

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO timeline (timestamp, data, filename, type, type_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, data_json, coverart_url, 'shazam', type_id))

# SELECT id, timestamp, time, place, record
for record in fetch(receipts_query):
    type_id = record[0]
    place = record[3]
    timestamp = f"{record[1]}T{record[2]}"
    filename = record[4]
    place_json = json.loads(record[5])
    record_json = json.loads(record[6])
    data_json = json.dumps({
        "place": place_json,
        **record_json  # This "splices" the properties of record_json into the final dictionary
    })
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO timeline (timestamp, place, data, filename, type, type_id)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, place, data_json, filename, 'receipt', type_id))

# SELECT id, timestamp, address
for record in fetch(pictures_query):
    type_id = record[0]
    timestamp = record[1]
    filename = record[2]
    place = record[3]
    address_json = json.loads(record[4]) if record[4] else {}
    data = json.loads(record[5]) if record[5] else {}  # Load the JSON object from record[5]

    # Blacklist of addresses to check against
    blacklist = ['2 thalia court', '35 south drive', '31 south drive']

    # Conditionally remove the 'address' key if its value is in the blacklist
    if address_json.get('address') in blacklist:
        del address_json['address']

    # Create a JSON-formatted string with title, artist, and link
    data_json = json.dumps({
        "place": address_json,
        **data  # Unpack the rest of the data object
    })

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO timeline (timestamp, filename, data, place, type, type_id)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, filename, data_json, place, 'picture', type_id))

for record in fetch(stories_query):
    type_id = record[0]
    date = record[1]
    time = record[2]
    category = record[3]
    text = record[4]
    dada_rank = record[5]
    sydney_rank = record[6]
    data = json.loads(record[7]) if record[7] else {}
    data.update({
        'category': category,
        'dada_rank': dada_rank,
        'sydney_rank': sydney_rank
    })

    if date and time:
        timestamp = f"{date}T{time}"
    elif isinstance(data, dict) and data.get('added_at') is not None:
        data.update({'spotify_add': True})
        timestamp = adjust_for_time_zone(adjust_to_local_time_from_z(data['added_at'], 4))
    else:
        timestamp = None

    data_json = json.dumps(data, indent=4)

    if (dada_rank and dada_rank <= 10) or (sydney_rank and sydney_rank <= 10) or \
        (category == 'songs' and timestamp and '2024-06-27T15:00:00' < timestamp < '2024-07-15T18:00:00'):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO timeline (timestamp, description, type, type_id, data)
            VALUES (?, ?, ?, ?, ?)
            ''', (timestamp, f"{category}: {text}", 'story', type_id, data_json))

# Commit and close the connection
conn.commit()
conn.close()
