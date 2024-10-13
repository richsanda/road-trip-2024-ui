import os
import json


def gather_files(directory):
    data = {}

    # Traverse the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        folder_name = os.path.relpath(root, directory)

        # Initialize a dictionary for this folder if it doesn't exist
        if folder_name not in data:
            data[folder_name] = {}

        # Filter to process only JSON files
        json_files = [file for file in files if file.endswith('.json')]

        for json_file in json_files:
            base_name = os.path.splitext(json_file)[0]

            # Initialize the wrapper object for this base name
            wrapper = {"json": None, "txt": None, "jpg": False}

            json_path = os.path.join(root, json_file)
            # Read and store the JSON content
            with open(json_path, 'r') as f:
                try:
                    wrapper["json"] = json.load(f)
                except json.JSONDecodeError:
                    wrapper["json"] = None

            # Check for corresponding TXT file
            txt_file = f"{base_name}.txt"
            txt_path = os.path.join(root, txt_file)
            if txt_file in files:
                with open(txt_path, 'r') as f:
                    wrapper["txt"] = f.read()

            # Check for corresponding JPG file
            jpg_file = f"{base_name}.jpg"
            if jpg_file in files:
                wrapper["jpg"] = True

            # Add the wrapper to the folder's dictionary
            data[folder_name][base_name] = wrapper

    return data


def write_json_to_file(data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)


if __name__ == "__main__":
    # Set your directory and output file
    directory = "/Users/rich.s/experiences/road-trip-2024"
    output_file = "output.json"

    # Gather the files in the directory
    json_data = gather_files(directory)

    # Write the data to a JSON file
    write_json_to_file(json_data, output_file)

    print(f"JSON data successfully written to {output_file}")
