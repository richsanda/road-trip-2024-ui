from connection import get_db_connection
import json


receipt_query = """
SELECT id, timestamp, filename, time, place, text, record 
FROM receipts
ORDER BY 
    timestamp ASC, 
    time ASC;
"""


def fetch_all_receipts():
    conn = get_db_connection()
    cursor = conn.execute(receipt_query)
    records = cursor.fetchall()
    conn.close()

    # Convert records to a list of dictionaries
    result = []
    for record in records:
        result.append({
            'id': record[0],
            'timestamp': record[1],
            'img_location': f"receipts/{record[2]}.jpg",
            'time': record[3],
            'place': record[4],
            'text': record[5],
            'record': json.loads(record[6]) if record[6] else None
        })

    return result


def update_receipt_timestamp(receipt_id, new_timestamp):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE receipts SET timestamp_override = ? WHERE id = ?', (new_timestamp, receipt_id))
    conn.commit()
    conn.close()
