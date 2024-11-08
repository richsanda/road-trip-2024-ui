from connection import get_db_connection
import json

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
    t.data,
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
        try:
            data = json.loads(record[6])
        except:
            data = None

        result.append({
            'id': record[0],
            'type': record[1],
            'type_id': record[2],
            'timestamp': record[3],
            'place': record[4],
            'description': record[5],
            'data': data,
            'filename': record[7],
            'keep': bool(record[8]),
            'notes': record[9]
        })

    return result


def fetch_timeline_with_notes_by_timestamp_range(start=None, end=None):
    conn = get_db_connection()

    where_clause = ""

    # Add conditions based on the presence of start and end parameters
    if start:
        where_clause += " AND timestamp >= ?"
    if end:
        where_clause += " AND timestamp <= ?"

    # Build the SQL query with optional WHERE clauses
    query = f"""
-- Query for timeline records
SELECT 
    t.id, 
    t.type,              -- Keep original type
    t.type_id, 
    CASE 
        WHEN n.date IS NOT NULL AND n.time IS NOT NULL THEN n.date || 'T' || n.time
        WHEN n.date IS NOT NULL THEN n.date || 'T' || strftime('%H:%M:%S', t.timestamp)
        WHEN n.time IS NOT NULL THEN strftime('%Y-%m-%d', t.timestamp) || 'T' || n.time
        ELSE t.timestamp
    END AS timestamp,
    t.place, 
    t.description, 
    t.data,
    t.filename, 
    NULL AS position,     -- NULL for position in timeline entries
    tn.keep, 
    tn.notes, 
    0 AS is_note,          -- 0 for timeline entries
    2 AS ordinal
FROM 
    timeline AS t
LEFT JOIN 
    timeline_notes AS tn 
ON 
    t.type = tn.type 
    AND t.type_id = tn.type_id
LEFT JOIN 
    notes AS n 
ON 
    t.type = n.type 
    AND t.type_id = n.type_id    
WHERE 
    1=1 AND (tn.keep = 1 OR t.type = 'story')
    {where_clause}
    
UNION 

SELECT 
    n.id, 
    n.type,              -- Keep original type from notes
    n.type_id, 
    CASE 
        WHEN n.date IS NOT NULL AND n.time IS NOT NULL THEN n.date || 'T' || n.time
        WHEN n.date IS NOT NULL THEN n.date || 'T' || strftime('%H:%M:%S', t.timestamp)
        WHEN n.time IS NOT NULL THEN strftime('%Y-%m-%d', t.timestamp) || 'T' || n.time
        ELSE t.timestamp
    END AS timestamp,
    NULL AS place,       -- No place for notes
    n.text AS description, -- Use text as the description for notes
    NULL AS data,        -- No data for notes
    NULL AS filename,    -- No filename for notes
    n.position,          -- Use position field from notes
    NULL AS keep,        -- NULL for keep, not applicable to notes
    NULL AS notes,       -- NULL for notes, as we're already in the notes table
    1 AS is_note,         -- 1 for notes
    CASE                -- Set ordinal based on position
        WHEN n.position = 'above' THEN 1
        WHEN n.position = 'below' THEN 3
    END AS ordinal
FROM 
    notes AS n
JOIN 
    timeline AS t 
ON 
    n.type = t.type 
    AND n.type_id = t.type_id
WHERE 
    1=1
    {where_clause}

-- Order by timestamp and position
ORDER BY 
    timestamp,          -- Sort by timestamp first
    ordinal;
    """

    # Prepare the parameters for the query
    params = tuple(filter(None, [start, end, start, end]))

    cursor = conn.execute(query, params)
    records = cursor.fetchall()
    conn.close()

    # Convert records to a list of dictionaries
    result = []
    for record in records:
        try:
            data = json.loads(record[6])
        except:
            data = None

        result.append({
            'id': record[0],
            'type': record[1],
            'type_id': record[2],
            'timestamp': record[3],
            'place': record[4],
            'description': record[5],
            'data': data,
            'filename': record[7],
            'position': record[8],
            'keep': bool(record[9]),
            'notes': record[10],
            'is_note': bool(record[11]),
            'ordinal': record[12]
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
