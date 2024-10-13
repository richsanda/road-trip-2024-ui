import openai
import os
import cv2
import pytesseract
from PIL import Image
from openai import OpenAI
import json

# Set the Tesseract command path if it's not in your PATH
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# Replace with your OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")


def ocr_image(image_path):
    # img = Image.open(image_path)
    # text = pytesseract.image_to_string(img)
    # return text

    # Open the image using cv2
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR with Tesseract
    custom_config = r'--oem 1 --psm 6'
    text = pytesseract.image_to_string(binary_image, config=custom_config)

    return text


def convert_text_to_fixed_with_openai(text, api_key):
    client = OpenAI(api_key=api_key)
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",  # Use the appropriate engine
        prompt=f"The following text is extracted from a scanned receipt using OCR, but contains errors and "
               f"inconsistencies. Please correct and format the text to resemble a clean and accurate receipt:"
               f"\n\n{text}\n\nCorrected text:",
        max_tokens=1500,
        temperature=0.1
    )
    return response.choices[0].text.strip()


def convert_receipt_text_to_json_with_openai(text, api_key):
    client = OpenAI(api_key=api_key)
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",  # Use the appropriate engine
        prompt=f"The following text is extracted from a scanned receipt using OCR. "
               f"Please correct the text without adding or assuming any additional information:\n\n{text}\n\n"
               f"Then, generate a JSON object that includes:\n"
               f"- A 'date' from the receipt (all receipts are in June or July 2024) in ISO format (YYYY-MM-DD)\n"
               f"- A 'time' from the receipt in military format (HH:MM)\n"
               f"- A verified 'address' of the business, if possible\n"
               f"- An itemized list ('items') of purchases with short descriptions\n"
               f"- A 'category' for the overall purchase (e.g., 'convenience', 'groceries', 'gas', 'restaurant', "
               f"'parking', ...)\n"
               f"- Any other relevant details.\n"
               f"Here is the corrected text and corresponding JSON object:\n\nCorrected text:\n\n"
               f"Corrected JSON object:",
        max_tokens=1500,
        temperature=0.1
    )
    return response.choices[0].text.strip()


def convert_receipt_json_to_www(text, api_key):
    prompt = f"""
Please generate JSON to characterize the provided JSON. Include these properties:

* "where" -- Where did the event represented by the provided JSON occur ? Please validate this information
             and correct as necessary since in some cases it was generated via OCR.
* "when" -- indicate when the event represented occurred. if it is a time range or span, include the end, too.
* "what" -- a short summary of the event represented by the JSON provided.

please return the JSON only, without explanation, as it needs to be program-readable.

**Example 1:**
Input:
{{
    "hotel_name": "Four Seasons Hotel Boston",
    "location": "200 Boyl ston St, Boston, MA 0216, USA",
    "check_in_time": "2024-08-15 15:00",
    "check_out_time": "2024-08-17 11:00",
    "room": {{
    "type": "Deluxe King Room",
      "rate": "450.00",
      "currency": "USD"
    }},
    "reservation_id": "ABC123456"
  }}
  
Output:
{{
    "where": {{
      "formatted_address": "Four Seasons Hotel Boston, 200 Boylston St, Boston, MA 02116, USA",
      "address": {{
        "business_name": "Four Seasons Hotel Boston",
        "line1": "200 Boylston St",
        "line2": null
        "city": "Boston",
        "state": "MA",
        "postal_code": "02116",
        "country": "USA"
      }}
    }},
    "when": {{
      "timestamp": "2024-08-15T15:00:00Z",
      "end_timestamp": "2024-08-17T11:00:00Z"
    }},
    "what": {{
      "description": "Hotel stay at Four Seasons in Boston."
    }}
}}

**Next Input:**
Input:
{text}
Output:
    """

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-4o-mini",
        max_tokens=500,
        temperature=0.2
    )
    return response.choices[0].message.content.strip()


def convert_life360_text_to_json_with_openai(text, api_key):
    prompt = f"""
convert a screen shot of a life 360 drive or trip from a phone into json.

**Example 1:**
Input:
4:56 MO Ae will 14% 0

Rich's 42 mi drive Gz)
4:17 pm - 5:24 pm (1 hr 6 min)

Brockton

Bridgewater

Rich's drive details

O |- 495, Massachusetts 4:17 PM

9 home 5:24 PM

Drive events

78 e
MPH a

Top High Phone Hard Rapid
Speed Speed Usage Braking Accel

Output:
{{
  "distance" : "42",
  "units" : "mi",
  "start_time" : "16:17",
  "end_time" : "17:24",
  "start_place" : "I-495, Massachusetts",
  "end_place" : "home",
  "duration_hours" : 1,
  "duration_minutes" : 6,
  "map_places" : ["Brockton", "Bridgewater"],
  "top_speed" : 78
}}

**Example 2:**
Input:
7:298@@->

€ Location Detail

eee Sie y ri aid ps! a |
=e oy, Meee | a 5 :
SEE S Peeyiheraierugy f

ls

Near 102 Wisconsin Avenue,
Montana
1:33 pm - 2:09 pm (35 min)

Add to Places

Output:
{{
  "start_time" : "13:33",
  "end_time" : "14:09",
  "place" : "102 Wisconsin Avenue, Montana",
  "duration_hours" : 0,
  "duration_minutes" : 35
}}

**Example 3:**
4:57 B MO Ae will 14% 0

<€ Rich's 67 mi trip
3:12 pm - 4:17 pm (1 hr 4 min)

Taunton

We
Nee, Ni

SOR
wal y/ Newport
2k) Ie
OZ Mo 4 __ Narragansett

Rich's trip details
O |- 90, Massachusetts 3:12 PM
9 |- 495, Massachusetts 4:17 PM

III O x

Output:
{{
  "distance" : "67",
  "units" : "mi",
  "start_time" : "15:12",
  "end_time" : "16:17",
  "start_place" : "I-90, Massachusetts",
  "end_place" : "I-495, Massachusetts",
  "duration_hours" : 1,
  "duration_minutes" : 4,
  "map_places" : ["Taunton", "Newport", "Narragansett"],
}}

**Next Input:**
{text}
Output:
"""

    client = OpenAI(api_key=api_key)
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=500,
        temperature=0.5
    )
    return response.choices[0].text.strip()


def process_file(image_path):
    text = ocr_image(image_path)
    # fixed_response = convert_text_to_fixed_with_openai(text, openai_api_key)
    json_response = convert_receipt_text_to_json_with_openai(text, openai_api_key)
    return json_response
    # try:
    #     json_data = json.loads(json_response)
    #     return json_data
    # except json.JSONDecodeError:
    #     print(f"Failed to decode JSON for {image_path}")
    #     return None


def process_directory(directory_path):
    result = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(directory_path, filename)

            print(f"Processing {image_path}...")
            # text = ocr_image(image_path)
            txt_path = change_extension_to_txt(image_path)
            # print(f"Writing OCR to {txt_path}...")
            # write_text_to_file(txt_path, text)

            # if filename.endswith(".txt"):
            #     txt_path = os.path.join(directory_path, filename)
            # Open the file in read mode
            with open(txt_path, 'r') as file:
                # Read the contents of the file
                text = file.read()
                json_response = convert_receipt_text_to_json_with_openai(text, openai_api_key)
                try:
                    json_data = json.loads(json_response)
                    json_path = change_extension_to_json(txt_path)
                    print(f"Writing json to {json_path}")
                    write_text_to_file(json_path, json_response)
                except json.JSONDecodeError:
                    print(f"Failed to decode JSON for {txt_path}")

    with open('receipts.json', 'w') as json_file:
        json.dump(result, json_file, indent=4)

    print("Processing complete. Results saved to receipts.json")


def process_directory_www(directory_path):
    result = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            json_path = os.path.join(directory_path, filename)

            print(f"Processing {json_path}...")

            with open(json_path, 'r') as file:
                # Read the contents of the file
                text = file.read()
                json_response = convert_receipt_json_to_www(text, openai_api_key)
                try:
                    json_data = json.loads(json_response)
                    json_www = change_extension_to_json(json_path)
                    print(f"Writing json to {json_www}")
                    write_text_to_file(json_www, json_response)
                except json.JSONDecodeError:
                    print(f"Failed to decode JSON from {json_response}")

    with open('receipts.json', 'w') as json_file:
        json.dump(result, json_file, indent=4)

    print("Processing complete. Results saved to receipts.json")


def change_extension_to_txt(file_path):
    # Get the base name without extension
    base_name = os.path.splitext(file_path)[0]
    # Create a new file path with .txt extension
    new_file_path = f"{base_name}.txt"
    return new_file_path


def change_extension_to_json(file_path):
    # Get the base name without extension
    base_name = os.path.splitext(file_path)[0]
    # Create a new file path with .txt extension
    new_file_path = f"{base_name}.json"
    return new_file_path


def change_extension_to_json(file_path):
    # Get the base name without extension
    base_name = os.path.splitext(file_path)[0]
    # Create a new file path with .txt extension
    new_file_path = f"{base_name}.json"
    return new_file_path


def write_text_to_file(file_path, text_content):
    with open(file_path, 'w') as file:
        file.write(text_content)


# Usage
# directory_path = 'path_to_your_directory'  # Replace with your directory path
# process_directory(directory_path)

# file_path = '/Users/rich.s/Documents/phone-2024-07-31/DCIM/Camera/20240731_205943.jpg'
file_path = '/Users/rich.s/experiences/road-trip-2024/receipts'
process_directory(file_path)
