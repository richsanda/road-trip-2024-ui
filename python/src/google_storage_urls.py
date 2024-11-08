import concurrent.futures
import sqlite3
from google.cloud import storage
from datetime import datetime, timedelta
from src.data.timeline import fetch_timeline_by_timestamp_range


def init_db():
    """Create a new SQLite database connection."""
    conn = sqlite3.connect('signed_urls.db')  # Change to your database path
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS signed_urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blob_name TEXT UNIQUE NOT NULL,
            signed_url TEXT NOT NULL,
            expiration TIMESTAMP NOT NULL
        )
    ''')
    conn.commit()
    return conn


def add_blob_names(entries, blob_name_key='blob_name'):
    for entry in entries:
        entry[blob_name_key] = f"images/{entry['type']}s/{entry['filename']}.jpg"
    return entries


def generate_signed_url(blob_name, expiration_seconds=3600):
    client = storage.Client()
    bucket = client.bucket('road-trip-2024')
    blob = bucket.blob(blob_name)

    # Calculate the expiration time (current time + expiration_seconds)
    expiration_time = datetime.utcnow() + timedelta(seconds=expiration_seconds)

    url = blob.generate_signed_url(expiration_time)  # 1 hour expiration
    return url


def cache_signed_url(blob_name, expiration_seconds=3600):
    """Insert or update the signed URL in the SQLite database."""
    signed_url = generate_signed_url(blob_name)

    # Create a new connection for this thread
    conn = init_db()
    current_time = datetime.now()
    expiration_time = current_time + timedelta(seconds=expiration_seconds)

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO signed_urls (blob_name, signed_url, expiration)
        VALUES (?, ?, ?)
        ON CONFLICT(blob_name) 
        DO UPDATE SET signed_url=excluded.signed_url, expiration=excluded.expiration
    ''', (blob_name, signed_url, expiration_time))

    conn.commit()
    conn.close()  # Close the connection after use
    return signed_url


def get_cached_url(blob_name):
    """Retrieve signed URL from cache if not expired."""
    # Create a new connection for this thread
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute('SELECT signed_url FROM signed_urls WHERE blob_name = ? AND expiration > ?',
                   (blob_name, datetime.now()))
    result = cursor.fetchone()
    conn.close()  # Close the connection after use
    return result[0] if result else None


def generate_urls(blob_dicts, blob_name_key='blob_name', signed_url_key='signed_url'):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(get_cached_url, blob_dict[blob_name_key]): blob_dict for blob_dict in blob_dicts
        }

        for future in concurrent.futures.as_completed(futures):
            blob_dict = futures[future]
            try:
                cached_url = future.result()

                if cached_url:
                    # Use cached URL if it exists
                    blob_dict[signed_url_key] = cached_url
                else:
                    # Generate a new signed URL and cache it
                    blob_name = blob_dict[blob_name_key]
                    blob_dict[signed_url_key] = cache_signed_url(blob_name)

            except Exception as exc:
                print(f'{blob_dict[blob_name_key]} generated an exception: {exc}')

    return blob_dicts


# Main execution
if __name__ == "__main__":
    pictures = fetch_timeline_by_timestamp_range('2024-06-27T00:00:00', '2024-06-27T23:00:00')
    add_blob_names(pictures)
    generate_urls(pictures, 'blob_name', 'signed_url')

    # Print signed URLs
    for pic in pictures:
        print(pic['signed_url'])
