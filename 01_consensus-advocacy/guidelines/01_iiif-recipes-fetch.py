import requests
import yaml
import csv
import os
import ast
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv()

GITHUB_API_URL = 'https://api.github.com/repos/IIIF/cookbook-recipes/contents/recipe'
BASE_URL = 'https://iiif.io/api/cookbook/recipe/'
RAW_CONTENT_BASE_URL = 'https://raw.githubusercontent.com/IIIF/cookbook-recipes/master/recipe/'

def fetch_directory_contents(url):
    token = os.getenv("GITHUB_TOKEN")
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_file_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_yaml_from_md(md_content):
    try:
        yaml_content = md_content.split('---')[1]
        return yaml.safe_load(yaml_content)
    except Exception as e:
        print(f"Error parsing YAML from Markdown: {e}")
        return {}

def fetch_json_files_in_directory(slug):
    """Fetch JSON files in the given directory and return their URLs."""
    directory_url = f"{GITHUB_API_URL}/{slug}"
    directory_contents = fetch_directory_contents(directory_url)
    json_files = [item['name'] for item in directory_contents if item['name'].endswith('.json')]
    return json_files

def safe_list(value):
    """Converts a value to a list if it's not already one, handling comma-separated strings."""
    if isinstance(value, str):
        if ',' in value:
            # If it's a comma-separated string, split it into a list
            return [item.strip() for item in value.split(',')]
        else:
            # If it's a single string (not comma-separated), return a list containing the string
            return [value]
    elif isinstance(value, list):
        # If it's already a list, return as is
        return value
    return []  # Return an empty list as a fallback

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    csv_filename = os.path.join(script_dir, 'recipes', 'iiif_recipes.csv')
    os.makedirs(os.path.dirname(csv_filename), exist_ok=True)

    directories = fetch_directory_contents(GITHUB_API_URL)

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'slug', 'url', 'json', 'recipe', 'topic', 'viewer', 'support', 'property'])

        for directory in directories:
            if directory['type'] == 'dir':
                slug = directory['name']
                recipe_url = f"{BASE_URL}{slug}/"
                json_files = fetch_json_files_in_directory(slug)
                
                md_url = urljoin(RAW_CONTENT_BASE_URL, f"{slug}/index.md")
                md_content = fetch_file_content(md_url)
                metadata = parse_yaml_from_md(md_content)

                if not metadata:
                    print(f"No metadata found for {slug}, skipping.")
                    continue
                
                topics = safe_list(metadata.get('topic', []))
                properties = safe_list(metadata.get('property', ''))
                viewer_data = metadata.get('viewers', [])
                if viewer_data is None:
                    viewer_data = []

                for topic in topics:
                    for viewer_item in viewer_data:
                        viewer, support = (viewer_item, 'Yes') if isinstance(viewer_item, str) else (viewer_item.get('id', ''), viewer_item.get('support', 'Yes'))
                        for prop in properties:
                            for json_file in json_files if json_files else ['manifest.json']:  # Default to 'manifest.json'
                                json_url = f"{recipe_url}{json_file}"
                                writer.writerow([
                                    metadata.get('id', ''),
                                    slug,
                                    recipe_url,
                                    json_url,
                                    metadata.get('title', ''),
                                    topic,
                                    viewer,
                                    support,
                                    prop,
                                ])

if __name__ == '__main__':
    main()