from src.data.connection import get_db_connection
import json


shazam_query = """
SELECT id, date, time, title, artist, link, track_key, about_track
FROM shazams
ORDER BY 
    date ASC, 
    time ASC;
"""


def fetch_all_shazams():
    conn = get_db_connection()
    cursor = conn.execute(shazam_query)
    records = cursor.fetchall()
    conn.close()

    # Convert records to a list of dictionaries
    result = []
    for record in records:

        # Parse the image_url JSON string
        image_data = json.loads(record[7]) if record[7] else {}

        # Extract the coverart URL if it exists
        coverart_url = image_data.get('images', {}).get('coverart', None)

        result.append({
            'id': record[0],
            'date': record[1],
            'time': record[2],
            'title': record[3],
            'artist': record[4],
            'link': record[5],
            'track_key': record[6],
            'image_url': coverart_url
        })

    return result
