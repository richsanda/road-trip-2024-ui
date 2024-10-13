import os
import json
from PIL import Image
import exifread
from datetime import datetime

def extract_exif_data(image_path):
    with open(image_path, 'rb') as image_file:
        tags = exifread.process_file(image_file)

    exif_data = {}

    # Extract GPS data if available
    gps_tags = ['GPS GPSLatitude', 'GPS GPSLongitude', 'GPS GPSAltitude',
                'GPS GPSLatitudeRef', 'GPS GPSLongitudeRef', 'GPS GPSAltitudeRef']
    gps_data = {}
    for tag in gps_tags:
        if tag in tags:
            gps_data[tag] = str(tags[tag])

    if gps_data:
        exif_data['GPS'] = gps_data

    # Extract timestamp
    if 'EXIF DateTimeOriginal' in tags:
        exif_data['Timestamp'] = str(tags['EXIF DateTimeOriginal'])

    # Add the filename
    exif_data['Filename'] = os.path.basename(image_path)

    return exif_data

def gps_to_decimal(degree, direction):
    d = float(degree[0])
    m = float(degree[1])

    # Handle the fractional seconds
    s_num, s_den = degree[2].split('/')
    s = float(s_num) / float(s_den)

    decimal = d + m / 60.0 + s / 3600.0
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal

def get_address_from_gps(gps_data):
    from geopy.geocoders import Nominatim
    if 'GPS GPSLatitude' in gps_data and 'GPS GPSLongitude' in gps_data:
        lat = gps_to_decimal(gps_data['GPS GPSLatitude'][1:-1].split(', '), gps_data['GPS GPSLatitudeRef'])
        lon = gps_to_decimal(gps_data['GPS GPSLongitude'][1:-1].split(', '), gps_data['GPS GPSLongitudeRef'])

        geolocator = Nominatim(user_agent="image_metadata_extractor")
        location = geolocator.reverse((lat, lon))
        return location.address if location else "Address not found"
    return None

def create_json_file_from_image(image_path, json_file_path):
    # Extract the EXIF data
    exif_data = extract_exif_data(image_path)

    try:
        # Add reverse geocoded address if GPS data is present
        if 'GPS' in exif_data:
            address = get_address_from_gps(exif_data['GPS'])
            if address:
                exif_data['Address'] = address
    except:
        print(f"error connecting for {image_path}")

    # Write data to json file
    with open(json_file_path, 'w') as json_file:
        json.dump(exif_data, json_file, indent=4)

def is_within_timestamp_range(exif_data, start_time, end_time):
    if 'Timestamp' in exif_data:
        timestamp = datetime.strptime(exif_data['Timestamp'], '%Y:%m:%d %H:%M:%S')
        return start_time <= timestamp <= end_time
    return False

def process_images_in_directory(directory, json_dir, start_time_str, end_time_str):
    start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S')
    end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S')

    #json_dir = os.path.join(directory, "json_files")
    #os.makedirs(json_dir, exist_ok=True)

    for filename in os.listdir(directory):
        if filename.lower().endswith('.jpg'):
            image_path = os.path.join(directory, filename)
            # Change extension to .json and create path for the json file
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            json_file_path = os.path.join(json_dir, f"{base_name}.json")
            exif_data = extract_exif_data(image_path)
            if is_within_timestamp_range(exif_data, start_time, end_time) and not os.path.exists(json_file_path):
                print(image_path)
                create_json_file_from_image(image_path, json_file_path)
            else:
                print(f"skipping {image_path}")

# Example usage
image_directory = '/Users/rich.s/Documents/phone-2024-07-31/DCIM/Camera'
image_json_directory = '/Users/rich.s/experiences/road-trip-2024/pictures'
start_time = "2024-06-27T15:00:00"
end_time = "2024-07-15T19:00:00"
process_images_in_directory(image_directory, image_json_directory, start_time, end_time)
