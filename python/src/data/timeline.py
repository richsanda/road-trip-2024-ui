from src.data.connection import get_db_connection


timeline_query = """
SELECT id, type, timestamp, place, description, filename
FROM timeline
WHERE timestamp > '2024-06-27T14:30' and timestamp < '2024-07-15T18:00' 
ORDER BY timestamp ASC
"""


def fetch_timeline():
    conn = get_db_connection()
    cursor = conn.execute(timeline_query)
    records = cursor.fetchall()
    conn.close()

    # Convert records to a list of dictionaries
    result = []
    for record in records:
        result.append({
            'id': record[0],
            'type': record[1],
            'timestamp': record[2],
            'place': record[3],
            'description': record[4],
            'filename': record[5]
        })

    return result


def fetch_timeline_by_timestamp_range(start=None, end=None):
    conn = get_db_connection()

    # Build the SQL query with optional WHERE clauses
    query = """
SELECT 
    t.id, 
    t.type, 
    t.type_id, 
    t.timestamp, 
    t.place, 
    t.description, 
    t.filename, 
    tn.keep,      -- Add keep field from timeline_notes
    tn.notes      -- Add notes field from timeline_notes
FROM 
    timeline AS t
LEFT JOIN 
    timeline_notes AS tn 
ON 
    t.type = tn.type 
    AND t.type_id = tn.type_id
WHERE 
    1=1 AND (tn.keep = 1 OR t.type = 'story')
    """  # Start with a non-filtered query

    # Add conditions based on the presence of start and end parameters
    if start:
        query += " AND t.timestamp >= ?"
    if end:
        query += " AND t.timestamp <= ?"

    query += " ORDER BY t.timestamp"

    # Prepare the parameters for the query
    params = tuple(filter(None, [start, end]))

    cursor = conn.execute(query, params)
    records = cursor.fetchall()
    conn.close()

    # Convert records to a list of dictionaries
    result = []
    for record in records:
        result.append({
            'id': record[0],
            'type': record[1],
            'type_id': record[2],
            'timestamp': record[3],
            'place': record[4],
            'description': record[5],
            'filename': record[6],
            'keep': bool(record[7]),
            'notes': record[8]
        })

    return result


def update_timeline_keep(type, type_id, new_keep):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Attempt to update the existing record
    cursor.execute('''
        UPDATE timeline_notes 
        SET keep = ? 
        WHERE type = ? AND type_id = ?
    ''', (new_keep, type, type_id))

    # Check if the update was successful
    if cursor.rowcount == 0:  # No rows were updated
        # Insert a new record if the record did not exist
        cursor.execute('''
            INSERT INTO timeline_notes (type, type_id, keep) 
            VALUES (?, ?, ?)
        ''', (type, type_id, new_keep))

    conn.commit()
    conn.close()
