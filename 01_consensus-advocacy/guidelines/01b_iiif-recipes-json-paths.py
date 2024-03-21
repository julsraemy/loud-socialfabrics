import pandas as pd
import requests
import json
import os
from collections import Counter

def fetch_json(url):
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}

def extract_keys(json_obj, prefix=''):
    keys = set()
    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            full_key = f'{prefix}.{k}' if prefix else k
            keys.add(full_key)
            keys.update(extract_keys(v, full_key))
    elif isinstance(json_obj, list):
        for item in json_obj:
            keys.update(extract_keys(item, prefix))
    return keys

def save_statistics_md(all_json_paths, all_content_links, filename):
    with open(filename, "w") as f:
        f.write("# JSON Paths and Content Links Statistics\n\n")
        f.write("## JSON Paths\n")
        for path, count in all_json_paths.items():
            f.write(f"- `{path}`: {count}\n")
        f.write("\n## Content Links\n")
        for link, count in all_content_links.items():
            f.write(f"- `{link}`: {count}\n")

# Load the CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'recipes', 'iiif_recipes.csv')
df = pd.read_csv(csv_path)

# Initialize counters for statistics
all_json_paths = Counter()
all_content_links = Counter()

# Process each JSON file
for _, row in df.iterrows():
    json_data = fetch_json(row['json'])
    json_paths = extract_keys(json_data)
    all_json_paths.update(json_paths)
    
    content_link = json_data.get('items', [{}])[0].get('items', [{}])[0].get('items', [{}])[0].get('body', {}).get('id', '')
    if content_link:
        all_content_links.update([content_link])

# Prepare data for CSV
json_path_data = [{'Type': 'JSON Path', 'Value': key, 'Occurrences': value} for key, value in all_json_paths.items()]
content_link_data = [{'Type': 'Content Link', 'Value': key, 'Occurrences': value} for key, value in all_content_links.items()]
combined_data = json_path_data + content_link_data

# Convert to DataFrame and save as CSV
stats_df = pd.DataFrame(combined_data)
stats_csv_path = os.path.join(script_dir, 'recipes', 'json_paths_content_links_stats.csv')
stats_df.to_csv(stats_csv_path, index=False)
print(f"Full JSON paths and content links statistics saved to CSV: {stats_csv_path}")

# Generate and save statistics in a Markdown file
statistics_md_path = os.path.join(script_dir, 'recipes', 'json_paths_content_links_statistics.md')
save_statistics_md(all_json_paths, all_content_links, statistics_md_path)
print(f"Statistics saved to MD: {statistics_md_path}")