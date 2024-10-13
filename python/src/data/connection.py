import sqlite3


# Helper function to connect to the database
def get_db_connection(database_location="database.db"):
    conn = sqlite3.connect(database_location)
    conn.row_factory = sqlite3.Row  # This allows us to access rows as dictionaries
    return conn
