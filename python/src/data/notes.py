import sqlite3
from src.content_util import extract_text_and_json

notes_query = """
SELECT id, type, type_id, position, text
FROM receipts
"""


class NotesData:

    def __init__(self, db_name='database.db'):
        self.db_name = db_name

    def connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def create_table(self):
        """Creates the 'notes' table if it doesn't exist."""
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                position TEXT NOT NULL,
                text TEXT NOT NULL
            )
        ''')
        print("Table 'notes' created successfully.")
        conn.commit()
        conn.close()

    def insert_note(self, type_id, type, position, text):
        """Inserts a single note into the 'notes' table."""
        conn = self.connection()
        cursor = conn.cursor()
        result = cursor.execute('''
            INSERT INTO notes (type_id, type, position, text)
            VALUES (?, ?, ?, ?)
        ''', (type_id, type, position, text))
        print(f"Note inserted: {text[:30]}...")
        conn.commit()
        conn.close()
        note_id = result.lastrowid
        self.update_note(note_id, {'text': text}) # to trigger the "fielded" info
        return note_id

    def fetch_all_notes(self):
        conn = self.connection()
        cursor = conn.execute(notes_query)
        records = cursor.fetchall()
        conn.close()

        # Convert records to a list of dictionaries
        result = []
        for record in records:
            result.append({
                'id': record[0],
                'type': record[1],
                'type_id': record[2],
                'position': record[3],
                'text': record[4]
            })

        return result

    def fetch_note_by_id(self, note_id):
        """Fetches a note by ID from the database."""
        conn = self.connection()
        cursor = conn.cursor()
        note = cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,)).fetchone()
        return note

    def update_note(self, note_id, data):
        """Updates a note based on provided fields."""

        conn = self.connection()
        cursor = conn.cursor()

        note = self.fetch_note_by_id(note_id)

        if note is None:
            return {"error": "Note not found"}

        update_fields = []
        update_values = []

        fields = {}
        # Collect fields to update
        if 'text' in data:
            text, fields = extract_text_and_json(data['text'])
            update_fields.append('text = ?')
            update_values.append(data['text'])
        # if 'category' in data:
        #     update_fields.append('category = ?')
        #     update_values.append(data['category'])
        if 'time' in data or 'time' in fields:
            update_fields.append('time = ?')
            update_values.append(fields.get('time') if 'time' in fields else data.get('time'))
        if 'date' in data or 'date' in fields:
            update_fields.append('date = ?')
            update_values.append(fields.get('date') if 'date' in fields else data.get('date'))

        if not update_fields:
            return {"message": "No fields to update"}

        update_query = 'UPDATE notes SET ' + ', '.join(update_fields) + ' WHERE id = ?'
        update_values.append(note_id)

        cursor.execute(update_query, update_values)
        conn.commit()
        conn.close()

        return True

    def delete_note_by_id(self, note_id):

        conn = self.connection()
        cursor = conn.cursor()

        if note_id and self.fetch_note_by_id(note_id):
            delete_query = 'DELETE from notes WHERE id = ?'
            cursor.execute(delete_query, (note_id,))
            conn.commit()
            conn.close()
            return True

        return False

