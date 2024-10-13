import pytesseract
import json
import cv2

from pytesseract import Output
from PIL import Image

def ocr_to_json(image_path):
    # Open the image file
    img = Image.open(image_path)

    # Perform OCR with DICT output
    data = pytesseract.image_to_data(img, output_type=Output.DICT)

    # Extract relevant information
    text_data = data['text']
    conf_data = data['conf']
    left_data = data['left']
    top_data = data['top']
    width_data = data['width']
    height_data = data['height']

    # Create a list to hold the items
    items = []
    for i in range(len(text_data)):
        if text_data[i].strip():  # Ignore empty text
            item = {
                'text': text_data[i],
                'bounding_box': {
                    'left': left_data[i],
                    'top': top_data[i],
                    'width': width_data[i],
                    'height': height_data[i]
                },
                'confidence': conf_data[i]
            }
            items.append(item)

    # Build a JSON structure similar to the itemized receipt
    receipt_data = {
        'items': items
    }

    return json.dumps(receipt_data, indent=4)

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# Path to the image you want to OCR
image_path = '/Users/rich.s/experiences/road-trip-2024/receipts/20240731_205318.jpg'
image_path = '/Users/rich.s/Documents/phone-2024-07-31/DCIM/Camera/20240731_205318.jpg'
# image_path = '/Users/rich.s/Documents/phone-2024-07-31/DCIM/Screenshots/Screenshot_20240723_170238_Life360.jpg'

# Open the image using PIL
#image = Image.open(image_path)
image = cv2.imread(image_path)

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding
_, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# OCR with Tesseract
custom_config = r'--oem 1 --psm 6'
text = pytesseract.image_to_string(binary_image, config=custom_config)

# Use pytesseract to do OCR on the image
#text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)

#print(ocr_to_json(image_path))