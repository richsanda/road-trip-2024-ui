from connection import get_db_connection


song_query = """
SELECT id, song_name, artist_name, image_link, song_link, ordinal
FROM songs
ORDER BY ordinal ASC;
"""


def fetch_all_songs():
    conn = get_db_connection()
    cursor = conn.execute(song_query)
    records = cursor.fetchall()
    conn.close()

    # Convert records to a list of dictionaries
    result = []
    for record in records:
        result.append({
            'id': record[0],
            'song_name': record[1],
            'artist_name': record[2],
            'image_link': record[3],
            'song_link': record[4]
        })

    return result
