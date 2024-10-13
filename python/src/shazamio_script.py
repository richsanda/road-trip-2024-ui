import sqlite3
import json
import asyncio
from shazamio import Shazam, Serialize
from src.data.shazams import fetch_all_shazams

# Connect to (or create) a SQLite3 database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()


async def main():
    shazam = Shazam()
    track_id = 552406075
    about_track = await shazam.track_about(track_id=track_id)
    serialized = Serialize.track(data=about_track)

    print(about_track)  # dict
    # print(serialized)  # serialized from dataclass factory

    for song in fetch_all_shazams():
        shazam_id = song['id']
        track_id = song['track_key']
        about_track = await shazam.track_about(track_id=track_id)
        serialized = Serialize.track(data=about_track)

        print(about_track)  # dict
        # print(serialized)  # serialized from dataclass factory

        cursor.execute("UPDATE shazams SET about_track = ? WHERE id = ?", (json.dumps(about_track), shazam_id))

    conn.commit()
    conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())