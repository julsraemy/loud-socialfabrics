import pandas as pd
import networkx as nx
from pyvis.network import Network
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the CSV file from the script's location
csv_path = os.path.join(script_dir, 'recipes', 'iiif_recipes.csv')

df = pd.read_csv(csv_path)

# Create a new graph
G = nx.Graph()

# Populate the graph with nodes and edges from the DataFrame
for _, row in df.iterrows():
    recipe_node = f"{row['id']}_{row['slug']}"
    viewer_node = row['viewer']
    G.add_node(recipe_node, title=row['recipe'], size=10, group='recipe')
    G.add_node(viewer_node, size=20, group='viewer')
    G.add_edge(recipe_node, viewer_node, title=row['support'])

# Convert to PyVis network
net = Network(height='100%', width='100%', bgcolor='#222222', font_color='white')
net.from_nx(G)
net.show_buttons(filter_=['physics'])  # Optionally enable physics configuration UI

# Save the interactive graph as an HTML file
html_path = os.path.join(script_dir, 'recipes', 'interactive_graph.html')
net.save_graph(html_path)
print(f"Graph saved to {html_path}")

