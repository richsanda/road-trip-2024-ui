from connection import get_db_connection
import json


map_query = """
SELECT id, timestamp, filename, start_time, end_time, start_place, end_place, map_places, hide 
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
"""


def fetch_all_maps():
    conn = get_db_connection()
    cursor = conn.execute(map_query)
    records = cursor.fetchall()
    conn.close()

    # Convert records to a list of dictionaries
    result = []
    for record in records:
        result.append({
            'id': record[0],
            'timestamp': record[1],
            'img_location': f"maps/{record[2]}.jpg",
            'start_time': record[3],
            'end_time': record[4],
            'start_place': record[5],
            'end_place': record[6],
            'map_places': json.loads(record[7]) if record[7] else None,
            'hide': bool(record[8])
        })

    return result


def update_map_timestamp(map_id, new_timestamp):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE maps SET timestamp = ? WHERE id = ?', (new_timestamp, map_id))
    conn.commit()
    conn.close()


def update_map_hide(map_id, new_hide):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE maps SET hide = ? WHERE id = ?', (new_hide, map_id))
    conn.commit()
    conn.close()
