import pandas as pd
import requests
from collections import defaultdict, Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

def fetch_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {}

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

def compare_key_sets(json_files):
    all_keys = {url: extract_keys(fetch_json(url)) for url in json_files}
    comparisons = defaultdict(dict)
    for url1, keys1 in all_keys.items():
        for url2, keys2 in all_keys.items():
            if url1 != url2:
                similarity = len(keys1.intersection(keys2)) / len(keys1.union(keys2))
                comparisons[url1][url2] = similarity
    return comparisons

def content_similarity_analysis(df):
    contents = []
    for _, row in df.iterrows():
        json_data = fetch_json(row['json'])
        properties = str(row['property']).split(',') if pd.notnull(row['property']) else []
        content = " ".join([str(json_data.get(prop.strip(), '')) for prop in properties])
        contents.append(content)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(contents)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix

# Load the CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'recipes', 'iiif_recipes.csv')
df = pd.read_csv(csv_path)

# Assuming the 'json' column contains JSON file URLs
json_files = df['json'].unique()

# Update DataFrame with additional data from JSON
df['JSON_Paths'] = ''
df['Label_en'] = ''
df['First_Content_Link'] = ''

for index, row in df.iterrows():
    json_data = fetch_json(row['json'])
    # Example JSON path extraction (modify as needed)
    json_paths = extract_keys(json_data)
    df.at[index, 'JSON_Paths'] = '; '.join(json_paths)
    # Extract label and first content link (modify JSONPath expressions as needed)
    df.at[index, 'Label_en'] = json_data.get('label', {}).get('en', [''])[0]
    first_item_id = json_data.get('items', [{}])[0].get('items', [{}])[0].get('items', [{}])[0].get('body', {}).get('id', '')
    df.at[index, 'First_Content_Link'] = first_item_id

# Compute and add similarity scores (this example does not integrate similarity scores into df directly due to complexity)

# Save the extended dataframe to a new CSV
extended_csv_path = os.path.join(script_dir, 'recipes', 'iiif_recipes_extended.csv')
df.to_csv(extended_csv_path, index=False)
print(f"Extended CSV saved to: {extended_csv_path}")

# Generating statistics on the most common JSON paths and content links
json_paths_list = '; '.join(df['JSON_Paths'].tolist()).split('; ')
path_counts = Counter(json_paths_list)
content_link_counts = Counter(df['First_Content_Link'].tolist())

# Save or print statistics as needed
print("Most Common JSON Paths:", path_counts.most_common(10))
print("Most Common Content Links:", content_link_counts.most_common(10))
