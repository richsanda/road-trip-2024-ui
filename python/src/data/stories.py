import sqlite3
import json
from src.content_util import extract_text_and_json


class StoriesData:

    def __init__(self, db_name='database.db'):
        self.db_name = db_name

    def connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def create_table(self):
        """Creates the 'stories' table if it doesn't exist."""
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                category TEXT NOT NULL,
                date TEXT,
                time TEXT,
                sydney_rank INTEGER,
                dada_rank INTEGER
            )
        ''')
        print("Table 'stories' created successfully.")
        conn.commit()
        conn.close()

    def insert_story(self, text, category, date=None, time=None, sydney_rank=None, dada_rank=None):
        """Inserts a single story into the 'stories' table."""
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO stories (text, category, date, time, sydney_rank, dada_rank)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (text, category, date, time, sydney_rank, dada_rank))
        print(f"Story inserted: {text[:30]}...")
        conn.commit()
        conn.close()

    def load_stories_from_file(self, file_path):
        """Loads stories from a JSON file and inserts them into the database."""
        with open(file_path, 'r') as f:
            data = json.load(f)

        for entry in data:
            text = entry.get("text")
            category = entry.get("category")
            sydney_rank = entry.get("sydney_rank")  # Or leave as None
            dada_rank = entry.get("dada_rank")  # Or leave as None

            self.insert_story(text, category, None, None, sydney_rank, dada_rank)

        print("Stories loaded from file and inserted into the database.")

    def fetch_stories(self, category=None, ranker=None):

        conn = self.connection()
        cursor = conn.cursor()

        if category and ranker:
            query = '''
            SELECT * FROM stories 
            WHERE category = ? 
            ORDER BY 
            CASE 
                WHEN ? = 'dada' THEN dada_rank
                WHEN ? = 'sydney' THEN sydney_rank
            END
            '''
            cursor.execute(query, (category, ranker, ranker,))
        elif category:
            query = '''
            SELECT * FROM stories 
            WHERE category = ? 
            ORDER BY 
            CASE WHEN date IS NULL THEN 1 ELSE 0 END,  -- Move NULL dates to the end
            date,                                     -- Sort by date
            CASE WHEN time IS NULL THEN 1 ELSE 0 END, -- Move NULL times to the end
            time                                      -- Sort by time
            '''
            cursor.execute(query, (category,))
        else:
            query = '''
            SELECT * FROM stories 
            ORDER BY 
            CASE WHEN date IS NULL THEN 1 ELSE 0 END,  -- Move NULL dates to the end
            date,                                     -- Sort by date
            CASE WHEN time IS NULL THEN 1 ELSE 0 END, -- Move NULL times to the end
            time                                      -- Sort by time         
            '''
            cursor = conn.cursor()
            cursor.execute(query)

        stories = cursor.fetchall()
        conn.close()

        # Convert the list of tuples into a list of dictionaries (JSON-like format)
        return [dict(story) for story in stories]

    def fetch_story_by_id(self, story_id):
        """Fetches a story by ID from the database."""
        conn = self.connection()
        cursor = conn.cursor()
        story = cursor.execute('SELECT * FROM stories WHERE id = ?', (story_id,)).fetchone()
        return story

    def update_story(self, story_id, data):
        """Updates a story based on provided fields."""

        conn = self.connection()
        cursor = conn.cursor()

        story = self.fetch_story_by_id(story_id)

        if story is None:
            return {"error": "Story not found"}

        update_fields = []
        update_values = []

        fields = {}

        # Collect fields to update
        if 'text' in data:
            text, fields = extract_text_and_json(data['text'])
            update_fields.append('text = ?')
            update_values.append(data['text'])
        if 'category' in data:
            update_fields.append('category = ?')
            update_values.append(data['category'])
        if 'date' in data:
            update_fields.append('date = ?')
            update_values.append(data['date'])
        if 'time' in data or 'time' in fields:
            update_fields.append('time = ?')
            update_values.append(fields.get('time') if 'time' in fields else data.get('time'))
        if 'sydney_rank' in data:
            update_fields.append('sydney_rank = ?')
            update_values.append(data['sydney_rank'])
        if 'dada_rank' in data:
            update_fields.append('dada_rank = ?')
            update_values.append(data['dada_rank'])

        if not update_fields:
            return {"message": "No fields to update"}

        update_query = 'UPDATE stories SET ' + ', '.join(update_fields) + ' WHERE id = ?'
        update_values.append(story_id)

        cursor.execute(update_query, update_values)
        conn.commit()
        conn.close()

        return True

    # Function to update story ranks in the database
    def update_story_ranks(self, category, ranker, ranked_data):

        # Connect to the SQLite database
        conn = self.connection()
        cursor = conn.cursor()

        try:

            # Prepare the field to update based on ranker
            rank_field = 'dada_rank' if ranker == 'dada' else 'sydney_rank'

            # Update each story's rank
            for story in ranked_data:
                story_id = story['id']
                new_rank = story['rank']

                cursor.execute(f'''
                    UPDATE stories
                    SET {rank_field} = ?
                    WHERE id = ? AND category = ?;
                ''', (new_rank, story_id, category))

            # Commit the changes and close the connection
            conn.commit()
            return True  # Return True if update is successful
        except Exception as e:
            print(f'Error updating ranks: {e}')
            return False
        finally:
            conn.close()  # Ensure the connection is closed

    def get_unique_categories(self):
        """Fetches unique categories from the 'stories' table."""
        self.cursor.execute('SELECT DISTINCT category FROM stories')
        categories = self.cursor.fetchall()
        category_list = [row['category'] for row in categories]
        return category_list

