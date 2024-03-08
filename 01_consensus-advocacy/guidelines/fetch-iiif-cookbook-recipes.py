import requests
import yaml
import csv
import json
from urllib.parse import urljoin

GITHUB_API_URL = 'https://api.github.com/repos/IIIF/cookbook-recipes/contents/recipe'
RAW_CONTENT_BASE_URL = 'https://raw.githubusercontent.com/IIIF/cookbook-recipes/master/recipe/'

def fetch_directory_contents(url):
    """Fetch the list of contents from a GitHub directory URL using the GitHub API."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def fetch_file_content(url):
    """Fetch the raw content of a file from a raw GitHub content URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_yaml_from_md(md_content):
    """Extract and parse the YAML front matter from a Markdown string."""
    try:
        yaml_content = md_content.split('---')[1]  # Extract YAML part
        return yaml.safe_load(yaml_content)
    except Exception as e:
        print(f"Error parsing YAML from Markdown: {e}")
        return {}

def analyze_json_files(recipe_slug):
    """Fetch and analyze JSON files for a given recipe. This is a placeholder for your JSON analysis logic."""
    # For simplicity, we're just returning a placeholder value. Expand this function based on your needs.
    return 'Example JSON Structure', 'Example Pattern', 'Example Data Type'

def main():
    csv_filename = 'iiif_recipes.csv'
    directories = fetch_directory_contents(GITHUB_API_URL)

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'slug', 'recipe', 'topic', 'viewer', 'support', 'property', 'json-structure', 'pattern', 'data-type'])

        for directory in directories:
            if directory['type'] == 'dir':
                slug = directory['name']
                md_url = urljoin(RAW_CONTENT_BASE_URL, f"{slug}/index.md")
                md_content = fetch_file_content(md_url)
                metadata = parse_yaml_from_md(md_content)

                # Simplified JSON analysis (replace with your actual logic)
                json_structure, pattern, data_type = analyze_json_files(slug)

                if metadata:
                    for viewer in metadata.get('viewers', []):
                        writer.writerow([
                            metadata.get('id', ''),
                            slug,
                            metadata.get('title', ''),
                            metadata.get('topic', ''),
                            viewer,
                            'Yes',  # Assuming 'Yes'; adjust based on your analysis
                            ','.join(metadata.get('property', [])),
                            json_structure,  # Placeholder or result of your JSON analysis
                            pattern,  # Placeholder or result of your JSON analysis
                            data_type,  # Placeholder or result of your JSON analysis
                        ])

if __name__ == '__main__':
    main()
