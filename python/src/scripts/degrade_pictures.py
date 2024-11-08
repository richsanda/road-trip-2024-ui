from PIL import Image
import os

def compress_image(input_path, output_path, quality=25):
    with Image.open(input_path) as img:
        img.save(output_path, "JPEG", quality=quality)

input_directory = "/Users/rich.s/experiences/road-trip-2024/pictures.2024-10-28"
output_directory = '/Users/rich.s/whateva/road-trip-2024-ui/images/pictures'

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Iterate through all .jpg files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(".jpg"):
        input_file = os.path.join(input_directory, filename)
        output_file = os.path.join(output_directory, filename)
        compress_image(input_file, output_file, quality=25)  # Adjust quality as needed

print("Compression completed.")
