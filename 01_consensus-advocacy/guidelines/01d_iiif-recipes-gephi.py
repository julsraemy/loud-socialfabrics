import pandas as pd
import networkx as nx
import os

# Same setup for script directory and CSV path
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'recipes', 'iiif_recipes.csv')

df = pd.read_csv(csv_path)

# Create a new graph
G = nx.Graph()

# Populate the graph
for _, row in df.iterrows():
    recipe_node = f"{row['id']}_{row['slug']}"
    viewer_node = row['viewer']
    G.add_node(recipe_node, label=row['recipe'], type='recipe')
    G.add_node(viewer_node, type='viewer')
    G.add_edge(recipe_node, viewer_node, support=row['support'])

# Write the graph to a GEXF file for use in Gephi
gexf_path = os.path.join(script_dir, 'recipes', 'graph_for_gephi.gexf')
nx.write_gexf(G, gexf_path)
