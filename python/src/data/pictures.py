from src.data.connection import get_db_connection


def fetch_pictures_by_timestamp_range(start=None, end=None):
    conn = get_db_connection()

    # Build the SQL query with optional WHERE clauses
    query = """
    SELECT pictures.*, timeline_notes.*
    FROM pictures
    LEFT JOIN timeline_notes
    ON pictures.id = timeline_notes.type_id
    AND timeline_notes.type = 'picture'
    WHERE timeline_notes.keep = 1

    """  # Start with a non-filtered query

    # Add conditions based on the presence of start and end parameters
    if start:
        query += " AND Timestamp >= ?"
    if end:
        query += " AND Timestamp <= ?"

    query += " ORDER BY Timestamp"

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
            'timestamp': record[1],
            'img_location': f"pictures/{record[2]}.jpg",
            'address': record[3]
        })

    return result

