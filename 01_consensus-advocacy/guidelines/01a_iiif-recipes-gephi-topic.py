import pandas as pd
import networkx as nx
import os
from collections import Counter

# Load the CSV file
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'recipes', 'iiif_recipes.csv')
df = pd.read_csv(csv_path)

# Create a new graph
G = nx.Graph()

# Prepare data for edges: count the occurrences of viewer-topic pairs
viewer_topic_pairs = df[['viewer', 'topic']].value_counts().reset_index(name='count')

# Add nodes and weighted edges based on the viewer-topic pairs
for _, row in viewer_topic_pairs.iterrows():
    viewer_node = row['viewer']
    topic_node = row['topic']
    weight = row['count']
    
    # Add nodes with their type as attribute
    G.add_node(viewer_node, type='viewer')
    G.add_node(topic_node, type='topic')
    
    # Add weighted edge with the count as label
    G.add_edge(viewer_node, topic_node, weight=weight, label=str(weight))

# Write the graph to a GEXF file for use in Gephi
gexf_path = os.path.join(script_dir, 'recipes', 'iiif_recipes_graph-topic.gexf')
nx.write_gexf(G, gexf_path)
