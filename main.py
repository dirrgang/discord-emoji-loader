import argparse
import json
import haralyzer
import requests
import os
from urllib.parse import urlparse, urlunparse
from tqdm import tqdm

# Function to download and store the file
def download_file(url, folder):
    filename = os.path.basename(url)
    filepath = os.path.join(folder, filename)
    
    # Skip if the file already exists
    if os.path.exists(filepath):
        print(f"Skipped (already exists): {filename}")
        return
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {filename}: {e}")
        return
    
    try:
        with open(filepath, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")
    except IOError as e:
        print(f"Error storing {filename}: {e}")
        return

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Download and store files from a HAR file containing "emoji" URLs.')
parser.add_argument('har_file', help='Path to the HAR file')
parser.add_argument('--folder', '-f', help='Destination folder for downloaded files', default='./')
args = parser.parse_args()

# Load the HAR file
har_file_path = args.har_file
with open(har_file_path, 'r') as file:
    har_data = json.load(file)

har_parser = haralyzer.HarParser(har_data)

# Extract URLs from the HAR file containing "emoji"
urls = [entry["request"]["url"] for entry in har_parser.har_data["entries"] if "emoji" in entry["request"]["url"]]

# Destination folder for downloaded files
folder = args.folder

# Create the destination folder if it doesn't exist
os.makedirs(folder, exist_ok=True)

# Download and store the files
for url in tqdm(urls, desc='Downloading', unit='file'):
    # Skip resizing part and query parameters
    parsed_url = urlparse(url)
    new_url = urlunparse(parsed_url._replace(query=''))
    download_file(new_url, folder)
