import pandas as pd
import requests
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

def fetch_json_as_text(url):
    """Fetch JSON content from the given URL and return as text. Append '.json' to URL if necessary."""
    if pd.isna(url):
        return ""  # Skip missing URLs
    if not url.endswith('.json'):
        url += '.json'  # Append '.json' to the URL if not present
    try:
        response = requests.get(url, allow_redirects=True)
        return response.text if response.status_code == 200 else ""
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

# Set paths for input CSV and output files
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'patterns', 'linked_art_patterns.csv')
gexf_path = os.path.join(script_dir, 'patterns', 'linked_art_patterns_similarity.gexf')
csv_output_path = os.path.join(script_dir, 'patterns', 'linked_art_patterns_similarity.csv')

# Load CSV data
df = pd.read_csv(csv_path)
patterns_info = df[['id', 'pattern']].drop_duplicates()

# Fetch JSON content as text for non-missing URLs
json_texts = [fetch_json_as_text(url) for url in df['json'] if pd.notna(url)]

# Compute content similarity
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(json_texts)
similarity_matrix = cosine_similarity(tfidf_matrix)

# Prepare data for GEXF and CSV output
G = nx.Graph()
similarity_scores = []

for i, row_i in patterns_info.iterrows():
    G.add_node(row_i['id'], label=row_i['pattern'])
    for j, row_j in patterns_info.iterrows():
        if i < j and j < len(json_texts):  # Avoid out-of-range errors and duplicate edges
            similarity_score = similarity_matrix[i, j]
            G.add_edge(row_i['id'], row_j['id'], weight=similarity_score)
            similarity_scores.append({
                'Pattern A': row_i['pattern'],
                'Pattern B': row_j['pattern'],
                'Similarity Score': similarity_score
            })

# Save graph to GEXF
nx.write_gexf(G, gexf_path)

# Save similarity scores to CSV
similarity_df = pd.DataFrame(similarity_scores)
similarity_df.to_csv(csv_output_path, index=False)

print(f"Content similarity graph saved to: {gexf_path}")
print(f"Content similarity scores saved to CSV: {csv_output_path}")
