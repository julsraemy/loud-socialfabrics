import pandas as pd
import os
import networkx as nx

# Load the CSV file
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'patterns', 'linked_art_patterns.csv')
df = pd.read_csv(csv_path)

# Initialize a NetworkX graph
G = nx.DiGraph()

# Process and add nodes and edges
for _, row in df.iterrows():
    # Node for the pattern
    pattern_id = f"pattern_{row['id']}"
    G.add_node(pattern_id, label=row['pattern'], description=row['description'], url=row['json'], category=row['category'])

    # Handle hierarchical relationships (category -> subcategory -> subsubcategory)
    if pd.notna(row['category']):
        category_id = f"category_{row['category']}"
        G.add_node(category_id, label=row['category'], type='category')
        G.add_edge(category_id, pattern_id)

    if pd.notna(row['subcategory']):
        subcategory_id = f"subcategory_{row['subcategory']}"
        G.add_node(subcategory_id, label=row['subcategory'], type='subcategory')
        G.add_edge(subcategory_id, pattern_id)

    if pd.notna(row['subsubcategory']):
        subsubcategory_id = f"subsubcategory_{row['subsubcategory']}"
        G.add_node(subsubcategory_id, label=row['subsubcategory'], type='subsubcategory')
        G.add_edge(subsubcategory_id, pattern_id)

# Export the graph to a GEXF file for Gephi
gexf_path = os.path.join(script_dir, 'patterns', 'linked_art_patterns_graph.gexf')
nx.write_gexf(G, gexf_path)
print(f"Graph saved as GEXF to: {gexf_path}")
