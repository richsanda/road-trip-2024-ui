import json


def build_json_from_outline(file_path):
    output = []
    category = None

    with open(file_path, 'r') as f:
        for line in f:
            stripped_line = line.strip()

            # Skip empty lines
            if not stripped_line:
                continue

            # Check if the line is a category (no indentation)
            if not line.startswith('  '):
                category = stripped_line
            else:
                # Add entry with category
                entry = stripped_line
                output.append({
                    "text": entry,
                    "category": category
                })

    return output


# Write output to a JSON file
def write_to_json(data, output_file):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)


# Example usage
file_path = 'top-10.txt'  # Replace with the path to your outline file
output_file = 'top-10.json'
data = build_json_from_outline(file_path)
write_to_json(data, output_file)

print(f"JSON array saved to {output_file}")
