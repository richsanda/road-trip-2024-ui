import re
import json


def extract_text_and_json(text):
    # Regular expression to match lines with format "word: value"
    prefixed_pattern = r'^\s*(\w+)\s*:\s*(.*)\s*$'

    # Initialize a dictionary to store key-value pairs
    json_result = {}

    # Initialize a list to store non-prefixed lines
    non_prefixed_lines = []

    # Split the text into lines and iterate over each line
    for line in text.splitlines():
        match = re.match(prefixed_pattern, line)
        if match:
            key = match.group(1).strip()  # Extract the key
            value = match.group(2).strip()  # Extract the value
            json_result[key] = value
        else:
            stripped_line = line.strip()
            if stripped_line:  # Ignore lines that are empty after stripping
                non_prefixed_lines.append(stripped_line)

    # Join the non-prefixed lines with a single newline
    condensed_text = "\n".join(non_prefixed_lines)

    # Replace multiple newlines (including newlines with spaces) with a single newline
    condensed_text = re.sub(r'\n+', '\n\n', condensed_text)

    # Return both the non-prefixed text and the JSON result
    return condensed_text, json_result


if __name__ == '__main__':

    # Example usage
    text_block = """
    name: John Doe
    
    Some additional information about John.
    
    
    age: 28
    
      Another piece of information.
      
    city: New York
    
    occupation: Developer
    
    
    More info here.
    """

    text, json_text = extract_text_and_json(text_block)
    print(text)
    print(json.dumps(json_text, indent=4))
