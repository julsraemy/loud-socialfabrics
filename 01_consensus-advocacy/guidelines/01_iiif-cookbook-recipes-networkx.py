import csv
import networkx as nx
import matplotlib.pyplot as plt

def read_csv(filename):
    """Read the CSV file and return a list of edges with attributes."""
    edges = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            # Including 'id' and 'property' as edge attributes for potential future use
            edges.append((row['recipe'], row['viewer'], {'support': row['support'], 'property': row['property'], 'id': row['id']}))
    return edges

def create_graph(edges):
    """Create a graph from the edges list."""
    G = nx.Graph()
    for edge in edges:
        recipe, viewer, attrs = edge
        G.add_node(recipe, type='recipe', topic=attrs.get('topic'))  # Optionally include 'topic' as a node attribute
        G.add_node(viewer, type='viewer')
        G.add_edge(recipe, viewer, **attrs)
    return G

def visualize_graph(G):
    """Visualize the graph with nodes and edges."""
    # Separate the nodes by type for different colors
    recipe_nodes = [node for node in G.nodes() if G.nodes[node]['type'] == 'recipe']
    viewer_nodes = [node for node in G.nodes() if G.nodes[node]['type'] == 'viewer']
    
    pos = nx.spring_layout(G)  # Use spring layout for positioning nodes
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, nodelist=recipe_nodes, node_color='skyblue', label='Recipes')
    nx.draw_networkx_nodes(G, pos, nodelist=viewer_nodes, node_color='lightgreen', label='Viewers')
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_size=8)
    
    plt.title('IIIF Cookbook Recipes and Viewers Network Graph')
    plt.legend()
    plt.axis('off')  # Hide the axis
    plt.show()

# Replace 'your_csv_file.csv' with the path to your CSV file
csv_filename = 'your_csv_file.csv'  # Ensure this matches your actual CSV file path and name
edges = read_csv(csv_filename)
G = create_graph(edges)
visualize_graph(G)
