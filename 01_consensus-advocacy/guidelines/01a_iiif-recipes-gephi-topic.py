import pandas as pd
import networkx as nx
import os
from collections import defaultdict

# Load the CSV file
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'recipes', 'iiif_recipes.csv')
df = pd.read_csv(csv_path)

# Create a new graph
G = nx.Graph()

# Count the occurrences of viewer-topic pairs for edge sizes
viewer_topic_pairs = df[['viewer', 'topic']].value_counts().reset_index(name='count')

# Determine viewer sizes by summing support across topics
viewer_sizes = df['viewer'].value_counts()

# Add nodes for viewers with size attribute, and topics
for viewer, size in viewer_sizes.items():
    G.add_node(viewer, type='viewer', size=size)

for topic in df['topic'].unique():
    G.add_node(topic, type='topic')

# Add edges with relative size based on support within topic
for _, row in viewer_topic_pairs.iterrows():
    viewer_node = row['viewer']
    topic_node = row['topic']
    relative_size = row['count'] / viewer_sizes[viewer_node]  # Normalize by total support
    G.add_edge(viewer_node, topic_node, size=relative_size*10, label=str(row['count']))  # Multiply by 10 for visibility

# Write the graph to a GEXF file for use in Gephi
gexf_path = os.path.join(script_dir, 'recipes', 'iiif_recipes_graph-topic.gexf')
nx.write_gexf(G, gexf_path)
