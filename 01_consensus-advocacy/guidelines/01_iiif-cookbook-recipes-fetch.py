import requests
import yaml
import csv
import os
from urllib.parse import urljoin
from dotenv import load_dotenv
load_dotenv()  # Take environment variables from .env.

# GitHub API URL for the IIIF cookbook recipes directory
GITHUB_API_URL = 'https://api.github.com/repos/IIIF/cookbook-recipes/contents/recipe'
# Base URL for raw content access
RAW_CONTENT_BASE_URL = 'https://raw.githubusercontent.com/IIIF/cookbook-recipes/master/recipe/'

def fetch_directory_contents(url):
    token = os.getenv("GITHUB_TOKEN")
    print(f"Using token: {token}")  # Debug print to check the token
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_file_content(url):
    """Fetch the raw content of a file from a raw GitHub content URL."""
    response = requests.get(url)  # Public raw content, no token needed here
    response.raise_for_status()
    return response.text

def parse_yaml_from_md(md_content):
    """Extract and parse the YAML front matter from a Markdown string."""
    try:
        # Extract YAML part from between the first two '---' delimiters
        yaml_content = md_content.split('---')[1]
        return yaml.safe_load(yaml_content)
    except Exception as e:
        print(f"Error parsing YAML from Markdown: {e}")
        return {}

def main():
    csv_filename = 'iiif_recipes.csv'
    directories = fetch_directory_contents(GITHUB_API_URL)

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'slug', 'recipe', 'topic', 'viewer', 'support', 'property'])

        for directory in directories:
            if directory['type'] == 'dir':
                slug = directory['name']
                md_url = urljoin(RAW_CONTENT_BASE_URL, f"{slug}/index.md")
                md_content = fetch_file_content(md_url)
                metadata = parse_yaml_from_md(md_content)

                if not metadata:
                    print(f"No metadata found for {slug}, skipping.")
                    continue
                
                properties = metadata.get('property', [''])  # Ensure there's at least one loop iteration even if no properties
                
                # Ensure 'viewers' is a list before iteration
                viewers = metadata.get('viewers', [])
                if not isinstance(viewers, list):
                    print(f"Invalid or missing 'viewers' in metadata for {slug}, might be an issue with the YAML content.")
                    viewers = []  # Set viewers to an empty list if it's not a list
                
                for property in properties:  # Direct iteration over the list
                    for viewer in viewers:
                        writer.writerow([
                            metadata.get('id', ''),
                            slug,
                            metadata.get('title', ''),
                            metadata.get('topic', ''),
                            viewer,
                            'Yes',  # Assuming 'Yes'; adjust based on your analysis
                            property,
                        ])

if __name__ == '__main__':
    main()