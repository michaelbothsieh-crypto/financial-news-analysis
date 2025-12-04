import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://finance.ettoday.net/news/3078288"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    print(f"Fetching {url} with verify=False...")
    response = requests.get(url, headers=headers, timeout=10, verify=False)
    print(f"Status Code: {response.status_code}")
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
