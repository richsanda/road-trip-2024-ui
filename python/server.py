from flask import Flask, Response, request, jsonify
import json
import os
from flask_cors import CORS
from datetime import datetime
from src.data.connection import get_db_connection
from src.data.maps import fetch_all_maps, update_map_timestamp, update_map_hide
from src.data.receipts import fetch_all_receipts, update_receipt_timestamp
from src.data.timeline import fetch_timeline_by_timestamp_range, update_timeline_keep
from src.data.pictures import fetch_pictures_by_timestamp_range
from src.data.shazams import fetch_all_shazams
from src.data.songs import fetch_all_songs
from src.data.messages import fetch_all_messages
from src.data.stories import StoriesData

app = Flask(__name__)
CORS(app)

stories_data = StoriesData("database.db")


def iso_to_pretty_date(iso_string):
    # Parse the ISO 8601 string to a datetime object
    dt = datetime.fromisoformat(iso_string)

    # Format the date and time to the desired format
    pretty_date = dt.strftime('%b %d, %-I:%M%p').lower()

    # Convert the AM/PM format to lowercase and remove the leading zero in hours
    pretty_date = pretty_date.replace('am', 'a').replace('pm', 'p')

    return pretty_date


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/health')
def health():
    return "OK", 200


@app.route('/receipts', methods=['GET'])
def get_receipts():
    records = fetch_all_receipts()
    response = json.dumps(records, indent=4)  # Pretty print with 4 spaces
    return Response(response, mimetype='application/json')


@app.route('/receipts/timestamp', methods=['POST'])
def post_receipt_timestamp():
    data = request.get_json()

    # Check if the necessary fields are in the request
    if not data or 'id' not in data or 'timestamp' not in data:
        return jsonify({'error': 'Bad request, missing id or timestamp'}), 400

    receipt_id = data['id']
    new_timestamp = data['timestamp']

    # Validate the timestamp format if necessary
    if not isinstance(new_timestamp, str):
        return jsonify({'error': 'Invalid timestamp format'}), 400

    # Update the timestamp in the database
    try:
        update_receipt_timestamp(receipt_id, new_timestamp)
        return jsonify({'success': True}), 200
    except Exception as e:
        print(f"Error updating timestamp: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/maps', methods=['GET'])
def get_maps():
    records = fetch_all_maps()
    response = json.dumps(records, indent=4)  # Pretty print with 4 spaces
    return Response(response, mimetype='application/json')


@app.route('/maps/update', methods=['POST'])
def post_map_update():
    data = request.get_json()

    # Check if the necessary fields are in the request
    if not data or 'id' not in data:
        return jsonify({'error': 'Bad request, missing'}), 400

    map_id = data['id']
    new_timestamp = data['timestamp'] if 'timestamp' in data else None
    new_hide = data['hide'] if 'hide' in data else None

    # Validate the timestamp format if necessary
    if new_timestamp is not None:
        if not isinstance(new_timestamp, str):
            return jsonify({'error': 'Invalid timestamp format'}), 400
        else:
            # Update the timestamp in the database
            try:
                update_map_timestamp(map_id, new_timestamp)
            except Exception as e:
                print(f"Error updating timestamp: {e}")
                return jsonify({'error': 'Internal server error'}), 500

    if new_hide is not None:
        # Validate the hide format if necessary
        if not isinstance(new_hide, bool):
            return jsonify({'error': 'Invalid hide format'}), 400
        else:
            # Update the timestamp in the database
            try:
                update_map_hide(map_id, new_hide)
            except Exception as e:
                print(f"Error updating timestamp: {e}")
                return jsonify({'error': 'Internal server error'}), 500

            return jsonify({'success': True}), 200


@app.route('/pictures', methods=['GET'])
def get_pictures():
    # Retrieve 'start' and 'end' parameters from the request
    start = request.args.get('start')
    end = request.args.get('end')

    # Fetch records based on the provided parameters
    records = fetch_pictures_by_timestamp_range(start, end)

    # Pretty print the JSON response
    response = json.dumps(records, indent=4)
    return Response(response, mimetype='application/json')


@app.route('/shazams', methods=['GET'])
def get_shazams():
    records = fetch_all_shazams()
    response = json.dumps(records, indent=4)  # Pretty print with 4 spaces
    return Response(response, mimetype='application/json')


@app.route('/songs', methods=['GET'])
def get_songs():
    records = fetch_all_songs()
    response = json.dumps(records, indent=4)  # Pretty print with 4 spaces
    return Response(response, mimetype='application/json')


@app.route('/messages', methods=['GET'])
def get_messages():
    records = fetch_all_messages()
    response = json.dumps(records, indent=4)  # Pretty print with 4 spaces
    return app.response_class(
        response=response,
        status=200,
        mimetype='application/json;charset=utf-8'
    )


# GET Endpoint to retrieve stories, filtered by category
@app.route('/stories', methods=['GET'])
def get_stories():
    category = request.args.get('category')  # Get the category filter from query parameters
    ranker = request.args.get('ranker')
    story_list = stories_data.fetch_stories(category, ranker)
    return jsonify(story_list)


# GET Endpoint to retrieve stories, filtered by category
@app.route('/stories/id', methods=['GET'])
def get_stories_by_id():
    story_id = request.args.get('id')  # Get the category filter from query parameters
    story = stories_data.fetch_story_by_id(story_id)
    return jsonify(dict(story))


@app.route('/stories', methods=['POST'])
def update_story():
    data = request.get_json()  # Get the JSON body from the POST request

    # Extract the ID (required)
    story_id = data.get('id')
    if not story_id:
        return jsonify({"error": "Story ID is required"}), 400

    stories_data.update_story(story_id, data)
    story = stories_data.fetch_story_by_id(story_id)

    return jsonify(dict(story))


@app.route('/stories/categories', methods=['GET'])
def get_unique_categories():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get unique categories
    cursor.execute('SELECT DISTINCT category FROM stories')
    categories = cursor.fetchall()

    conn.close()

    # Format the result as a list of category names
    category_list = [row['category'] for row in categories]

    return jsonify(category_list)


@app.route('/timeline', methods=['GET'])
def get_timeline():

    # Retrieve 'start' and 'end' parameters from the request
    start = request.args.get('start')
    end = request.args.get('end')

    records = fetch_timeline_by_timestamp_range(start, end)
    response = json.dumps(records, indent=4)  # Pretty print with 4 spaces
    return app.response_class(
        response=response,
        status=200,
        mimetype='application/json;charset=utf-8')


@app.route('/timeline/update', methods=['POST'])
def post_timeline_update():
    data = request.get_json()

    # Check if the necessary fields are in the request
    if not data or 'type' not in data or 'type_id' not in data:
        return jsonify({'error': 'Bad request, missing'}), 400

    type = data['type']
    type_id = data['type_id']
    new_keep = data['keep'] if 'keep' in data else None

    if new_keep is not None:
        # Validate the hide format if necessary
        if not isinstance(new_keep, bool):
            return jsonify({'error': 'Invalid hide format'}), 400
        else:
            # Update the timestamp in the database
            try:
                update_timeline_keep(type, type_id, new_keep)
            except Exception as e:
                print(f"Error updating timestamp: {e}")
                return jsonify({'error': 'Internal server error'}), 500

            return jsonify({'success': True}), 200


@app.route('/stories/ranks', methods=['POST'])
def update_ranks():
    # Get the JSON data from the request
    data = request.get_json()

    # Extract category and ranker from query parameters
    category = request.args.get('category')
    ranker = request.args.get('ranker')

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Validate the incoming data
    if not isinstance(data, list):
        return jsonify({'error': 'Data should be a list of ranked stories'}), 400

    for story in data:
        if 'id' not in story or 'rank' not in story:
            return jsonify({'error': 'Each story must contain an id and a rank'}), 400

    # Call the function to update story ranks
    success = stories_data.update_story_ranks(category, ranker, data)

    if success:
        return jsonify({'message': 'Ranks updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update ranks'}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", os.environ.get("FLASK_RUN_PORT", 5000)))  # Default to 5000 if no PORT
    app.run(host="0.0.0.0", port=port)

