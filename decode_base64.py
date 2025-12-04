import base64
import re

url = "https://news.google.com/rss/articles/CBMiUkFVX3lxTE5hX2dIdzQtVHlUWjVYcm90MnhFOEZ1eE9DNXBjMk1LVEpRbExIVTZQLWVOVEh5WTRra1VUNzVPMExwOWNnQWZRX252eEVWcGpHZXfSAW5BVV95cUxQdnBBMmthcXZHQVRmTHhhRWpvbHA5WHlZbmZsOHRGWWZGajN5R0Rkc19IdmFCNEtEcExJUVRlNDdUNEZHRkhJLWVqSjF0RlZlRVBzRS1CaFdvZ2lXdnVwa2Vrdk95RzQ1ODJaZEMyQQ?oc=5"

# Extract the base64 part
match = re.search(r'articles/([^?]+)', url)
if match:
    b64_str = match.group(1)
    # Fix padding
    padding = len(b64_str) % 4
    if padding:
        b64_str += '=' * (4 - padding)
    
    try:
        decoded_bytes = base64.urlsafe_b64decode(b64_str)
        print(f"Decoded bytes: {decoded_bytes}")
        # Try to find http in the bytes
        decoded_str = decoded_bytes.decode('latin1', errors='ignore')
        print(f"Decoded string: {decoded_str}")
        
        url_match = re.search(r'(https?://\S+)', decoded_str)
        if url_match:
            print(f"Found URL: {url_match.group(1)}")
    except Exception as e:
        print(f"Error decoding: {e}")
