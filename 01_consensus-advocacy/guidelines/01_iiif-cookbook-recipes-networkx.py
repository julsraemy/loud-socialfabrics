import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the CSV file from the script's location
csv_path = os.path.join(script_dir, 'recipes', 'iiif_recipes.csv')

df = pd.read_csv(csv_path)

# Create a new graph
G = nx.Graph()

# Add nodes and edges from the DataFrame
for index, row in df.iterrows():
    recipe_node = f"{row['id']}_{row['slug']}"
    viewer_node = row['viewer']
    G.add_node(recipe_node, type='recipe', label=row['recipe'])
    G.add_node(viewer_node, type='viewer')
    G.add_edge(recipe_node, viewer_node, support=row['support'])

# Draw the graph
plt.figure(figsize=(20, 15))  # Increase figure size
pos = nx.spring_layout(G, k=0.15, iterations=20)  # Adjust layout parameters

nx.draw_networkx_nodes(G, pos, nodelist=[n for n, d in G.nodes(data=True) if d['type'] == 'recipe'], node_color='skyblue', label='Recipes')
nx.draw_networkx_nodes(G, pos, nodelist=[n for n, d in G.nodes(data=True) if d['type'] == 'viewer'], node_color='lightgreen', label='Viewers')

edges_yes = [(u, v) for u, v, d in G.edges(data=True) if d['support'] == 'Yes']
edges_partial = [(u, v) for u, v, d in G.edges(data=True) if d['support'] == 'Partial']
nx.draw_networkx_edges(G, pos, edgelist=edges_yes, edge_color='blue', style='solid', label='Full Support')
nx.draw_networkx_edges(G, pos, edgelist=edges_partial, edge_color='red', style='dashed', label='Partial Support')

nx.draw_networkx_labels(G, pos)

plt.title('IIIF Recipe-Viewer Graph with Support Levels')
plt.axis('off')
plt.legend()
plt.tight_layout()

# Specify the output paths for SVG and PDF relatively
svg_path = os.path.join(script_dir, 'recipes', 'recipe_viewer_graph.svg')
pdf_path = os.path.join(script_dir, 'recipes', 'recipe_viewer_graph.pdf')

# Save the graph as SVG and PDF
plt.savefig(svg_path)
plt.savefig(pdf_path)

plt.show()
