import pandas as pd
import requests
import os
import json
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def fetch_json(url):
    """Fetch JSON data from a given URL."""
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    return response.json()

def extract_keys(json_obj, prefix=''):
    """Recursively extract all keys from a JSON object."""
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
    """Compare the key sets of multiple JSON files."""
    all_keys = {url: extract_keys(fetch_json(url)) for url in json_files}
    comparisons = defaultdict(dict)
    for url1, keys1 in all_keys.items():
        for url2, keys2 in all_keys.items():
            if url1 != url2:
                similarity = len(keys1.intersection(keys2)) / len(keys1.union(keys2))
                comparisons[url1][url2] = similarity
    return comparisons

def content_similarity_analysis(df):
    """Analyze content similarity for specified properties in the DataFrame."""
    contents = []
    for _, row in df.iterrows():
        json_data = fetch_json(row['json'])
        content = " ".join([str(json_data.get(prop, '')) for prop in row['property'].split(',')])
        contents.append(content)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(contents)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix

# Load the CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'recipes', 'iiif_recipes.csv')
df = pd.read_csv(csv_path)

# Assuming the 'json' column contains unique JSON file URLs
json_files = df['json'].unique()

# Key Set Similarity Analysis
key_set_comparisons = compare_key_sets(json_files)
print("Key Set Similarity Analysis:")
for url, comparisons in key_set_comparisons.items():
    print(f"{url}:")
    for comp_url, similarity in comparisons.items():
        print(f"  {comp_url}: {similarity:.2f}")

# Content Similarity Analysis
# Note: Adjust property extraction as per your JSON structure and requirements
print("\nContent Similarity Analysis:")
similarity_matrix = content_similarity_analysis(df)
print(similarity_matrix)