from openai import OpenAI
import os
import json
from pathlib import Path


# Replace with your OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

system_instructions_file = "prompts/convert_life360_map_to_json.2.txt"

with open(system_instructions_file, "r") as file:
    system_instructions = file.read()


def convert_life360_to_json(text, api_key):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": system_instructions
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
        temperature=0.2,
        max_tokens=1460,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "json_object"
        }
    )
    return json.loads(response.choices[0].message.content)


# Directory containing the .txt files
directory = "/Users/rich.s/experiences/road-trip-2024/maps-images/"
directory2 = "/Users/rich.s/experiences/road-trip-2024/maps/"

# Iterate over all .txt files in the directory
for txt_file_path in Path(directory).glob("*.txt"):
    # Read the content of the .txt file
    with open(txt_file_path, "r") as txt_file:
        text_content = txt_file.read()

    with open(os.path.join(directory2, os.path.basename(txt_file_path)), "r") as txt_file2:
        text_content2 = txt_file2.read()

    # Convert the text using your function
    json_data = convert_life360_to_json(f"{text_content}\n---\n{text_content2}", openai_api_key)

    # Define the output .json file path (same name but .json extension)
    json_file_path = txt_file_path.with_suffix(".json")

    # Save the JSON response to the new .json file
    with open(json_file_path, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

    print(f"Processed: {txt_file_path} -> {json_file_path}")
