import pandas as pd
import networkx as nx
import os

# Load the CSV file
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'recipes', 'iiif_recipes.csv')
df = pd.read_csv(csv_path)

# Create a new graph
G = nx.Graph()

# Add nodes and edges from the DataFrame
for _, row in df.iterrows():
    recipe_node = f"{row['id']}_{row['slug']}"
    viewer_node = row['viewer']
    # Node attributes
    G.add_node(recipe_node, label=row['recipe'], slug=row['slug'], type='recipe', url=row['url'])
    G.add_node(viewer_node, type='viewer')
    # Edge attributes
    G.add_edge(recipe_node, viewer_node, support=row['support'], property=row['property'])

# Write the graph to a GEXF file for use in Gephi
gexf_path = os.path.join(script_dir, 'recipes', 'iiif_recipes_graph.gexf')
nx.write_gexf(G, gexf_path)