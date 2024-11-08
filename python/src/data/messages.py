from connection import get_db_connection
from datetime import datetime

message_query = """
SELECT id, sender_name, timestamp_ms, content
FROM messages
ORDER BY timestamp_ms ASC;
"""


def fetch_all_messages():
    conn = get_db_connection()
    cursor = conn.execute(message_query)
    records = cursor.fetchall()
    conn.close()

    # Convert records to a list of dictionaries
    result = []
    for record in records:
        timestamp = datetime.utcfromtimestamp(record[2] / 1000).isoformat('T')
        result.append({
            'id': record[0],
            'sender_name': record[1],
            'timestamp_ms': record[2],
            'timestamp': timestamp,
            'content': record[3]
        })

    return result
