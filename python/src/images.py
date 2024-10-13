import os
import json
from PIL import Image
import exifread

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

def create_json_file_from_image(image_path, json_dir):
    # Extract the EXIF data
    exif_data = extract_exif_data(image_path)

    # Change extension to .json and create path for the json file
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    json_file_path = os.path.join(json_dir, f"{base_name}.json")

    # Write data to json file
    with open(json_file_path, 'w') as json_file:
        json.dump(exif_data, json_file, indent=4)

def process_images_in_directory(directory):
    json_dir = os.path.join(directory, "json_files")
    os.makedirs(json_dir, exist_ok=True)

    for filename in os.listdir(directory):
        if filename.lower().endswith('.jpg'):
            image_path = os.path.join(directory, filename)
            create_json_file_from_image(image_path, json_dir)

# Example usage
image_directory = '/Users/rich.s/experiences/road-trip-2024/pictures'
process_images_in_directory(image_directory)
