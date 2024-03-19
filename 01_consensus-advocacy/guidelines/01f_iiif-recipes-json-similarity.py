import pandas as pd
import requests
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

def fetch_json_as_text(url):
    response = requests.get(url)
    return response.text if response.status_code == 200 else ''

def compute_content_similarity(json_texts):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(json_texts)
    return cosine_similarity(tfidf_matrix)

# Load the CSV and drop duplicates based on the 'recipe' column to ensure uniqueness
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'recipes', 'iiif_recipes.csv')
df = pd.read_csv(csv_path).drop_duplicates(subset=['recipe'])

# Fetch JSON content as text for each JSON file URL after deduplication
json_texts = [fetch_json_as_text(url) for url in df['json']]
recipe_names = df['recipe'].tolist()

# Compute content similarity
similarity_matrix = compute_content_similarity(json_texts)

# Initialize a NetworkX graph for GEXF output and a list to save similarity scores
G = nx.Graph()
similarity_data = []

# Populate the graph with nodes and similarity scores as edge weights
for i, name_a in enumerate(recipe_names):
    G.add_node(i, label=name_a)
    for j, name_b in enumerate(recipe_names):
        if i != j:
            G.add_edge(i, j, weight=similarity_matrix[i][j])
            similarity_data.append({"Recipe A": name_a, "Recipe B": name_b, "Similarity Score": similarity_matrix[i][j]})

# Save the graph to GEXF
gexf_path = os.path.join(script_dir, 'recipes', 'json_content_similarity_graph.gexf')
nx.write_gexf(G, gexf_path)

# Convert similarity data to DataFrame and save as CSV
similarity_df = pd.DataFrame(similarity_data)
similarity_csv_path = os.path.join(script_dir, 'recipes', 'content_similarity_scores.csv')
similarity_df.to_csv(similarity_csv_path, index=False)

# Save similarity scores to Markdown file
md_path = os.path.join(script_dir, 'recipes', 'content_similarity_report.md')
with open(md_path, 'w') as md_file:
    md_file.write("# Content Similarity Report\n\n")
    for i, name_a in enumerate(recipe_names):
        md_file.write(f"## {name_a}\n")
        for j, name_b in enumerate(recipe_names):
            if i < j:  # Prevent duplication
                md_file.write(f"- Similarity with {name_b}: {similarity_matrix[i][j]:.2f}\n")
        md_file.write("\n")

print(f"Content similarity graph saved as GEXF to: {gexf_path}")
print(f"Content similarity report saved to MD: {md_path}")
print(f"Content similarity scores saved to CSV: {similarity_csv_path}")
