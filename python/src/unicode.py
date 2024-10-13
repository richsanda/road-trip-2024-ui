# The doubly-encoded string
encoded_string = "\u00e2\u009d\u00a4\u00ef\u00b8\u008f"

# First, encode it using Latin-1
decoded_bytes = encoded_string.encode('latin1')

# Then decode it back using UTF-8
final_string = decoded_bytes.decode('utf-8')

print(final_string)  # This should print the correct emoji
