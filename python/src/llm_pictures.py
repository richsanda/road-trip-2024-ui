from openai import OpenAI
import json
import os
import sqlite3
from src.data.pictures import fetch_pictures_by_timestamp_range
from src.data.receipts import fetch_all_receipts
from src.data.maps import fetch_all_maps
from concurrent.futures import ThreadPoolExecutor
from functools import partial

# Replace with your OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

def convert_address_to_json(text, api_key):

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": """
You convert location descriptions into a simple json form with props address, city, county, state, postal, business. 
Favor states over cities if ambiguous ("new york" without context should be assumed a state). 
Put the remainder into address if confused ("I-90, US 87, US 212" can go into address).
Use all small chars. Omit fields with empty values. No markup frame. Examples:
input:
28, Pine Ridge II, Town of Clifton Park, Saratoga County, New York, 12065, United States
output:
{
  "address": "28 pine ridge ii",
  "city": "clifton park",
  "county":"saratoga county",
  "state": "ny",
  "postal": "12065"
}
input:
Wheat Montana Kalispell 405 Main Street, Kalispell, MT 59901
output:
{
  "address": "405 main street",
  "city": "kalispell",
  "state": "mt",
  "postal": "59901",
  "business": "wheat montana kalispell"
}
input:
I-90, US 87, US 212, Montana
output:
{
  "address": "I-90, US 87, US 212",
  "state": "mt"
}                
                        """
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ],
        temperature=0,
        max_tokens=1460,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )
    return json.loads(response.choices[0].message.content)


def update_address_json(db_path, record_id, address_data):
    # Convert the JSON object to a string
    address_json_str = json.dumps(address_data)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to update the address_json column
    query = """
    UPDATE pictures
    SET address_json = ?
    WHERE id = ?;
    """

    # Execute the query
    cursor.execute(query, (address_json_str, record_id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def update_place_json(db_path, record_id, place_data):
    # Convert the JSON object to a string
    place_json_str = json.dumps(place_data)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to update the place_json column
    query = """
    UPDATE receipts
    SET place_json = ?
    WHERE id = ?;
    """

    # Execute the query
    cursor.execute(query, (place_json_str, record_id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def update_start_place_json(db_path, record_id, place_data):
    # Convert the JSON object to a string
    place_json_str = json.dumps(place_data)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to update the place_json column
    query = """
    UPDATE maps
    SET start_place_json = ?
    WHERE id = ?;
    """

    # Execute the query
    cursor.execute(query, (place_json_str, record_id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def update_end_place_json(db_path, record_id, place_data):
    # Convert the JSON object to a string
    place_json_str = json.dumps(place_data)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to update the place_json column
    query = """
    UPDATE maps
    SET end_place_json = ?
    WHERE id = ?;
    """

    # Execute the query
    cursor.execute(query, (place_json_str, record_id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Function to handle the process for each picture
def process_picture(picture, db_path, openai_api_key):
    address_json = convert_address_to_json(picture["address"], openai_api_key)
    update_address_json(db_path, picture["id"], address_json)
    print(json.dumps(address_json))


# Function to handle the process for each picture
def process_receipt(receipt, db_path, openai_api_key):
    place_json = convert_address_to_json(receipt["place"], openai_api_key)
    update_place_json(db_path, receipt["id"], place_json)
    print(json.dumps(place_json))


# Function to handle the process for each picture
def process_map(record, db_path, openai_api_key):
    if record["end_place"]:
        place_json = convert_address_to_json(record["end_place"], openai_api_key)
        update_end_place_json(db_path, record["id"], place_json)
        print(json.dumps(place_json))


# Multithreading with 5 workers
def multithread_process_records(records, db_path, openai_api_key):
    # Use ThreadPoolExecutor to run the tasks concurrently
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Partial function to pass db_path and openai_api_key automatically
        process_func = partial(process_map, db_path=db_path, openai_api_key=openai_api_key)
        # Submit each picture processing task to the executor
        executor.map(process_func, records)


# pictures = fetch_pictures_by_timestamp_range("2024-06-27T14:00:00", "2024-07-15T20:00:00")
# print(f"found {len(pictures)} pictures... here goes :)")
# receipts = fetch_all_receipts()
# print(f"found {len(receipts)} receipts... here goes :)")
maps = fetch_all_maps()
print(f"found {len(maps)} maps... here goes :)")
multithread_process_records(maps, db_path="database.db", openai_api_key=openai_api_key)
