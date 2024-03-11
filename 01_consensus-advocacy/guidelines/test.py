from pyvis.network import Network
import pandas as pd
import os

def create_graph(df, graph_type):
    net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')
    net.force_atlas_2based()
    net.show_buttons(filter_=['physics'])

    if graph_type == 'recipe-viewer':
        for _, row in df.iterrows():
            recipe_node = row['slug']
            viewer_node = f"viewer_{row['viewer']}"
            net.add_node(recipe_node, label=recipe_node, size=15, group='recipe', title=row['recipe'])
            net.add_node(viewer_node, label=row['viewer'], size=25, group='viewer', title=row['viewer'])
            net.add_edge(recipe_node, viewer_node, title=f"Support: {row['support']}")

    elif graph_type == 'recipe-topic':
        unique_topics = df.drop_duplicates(subset=['slug', 'topic'])
        for _, row in unique_topics.iterrows():
            recipe_node = row['slug']
            topic_node = f"topic_{row['topic']}"
            net.add_node(recipe_node, label=recipe_node, size=15, group='recipe', title=row['recipe'])
            net.add_node(topic_node, label=row['topic'], size=20, group='topic', title=row['topic'])
            net.add_edge(recipe_node, topic_node)

    elif graph_type == 'recipe-property':
        for _, row in df.iterrows():
            recipe_node = row['slug']
            properties = str(row['property']).split(',')
            for prop in properties:
                prop_cleaned = prop.strip()
                if prop_cleaned:
                    property_node = f"property_{prop_cleaned}"
                    net.add_node(recipe_node, label=recipe_node, size=15, group='recipe', title=row['recipe'])
                    net.add_node(property_node, label=prop_cleaned, size=20, group='property', title=prop_cleaned)
                    net.add_edge(recipe_node, property_node)

    html_filename = f'interactive_graph_{graph_type}.html'
    html_path = os.path.join(script_dir, 'recipes', html_filename)
    net.save_graph(html_path)
    print(f"Graph saved to: {html_path}")

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'recipes', 'iiif_recipes.csv')

# Load data
df = pd.read_csv(csv_path)

# Generate specific graphs for recipe-viewer, recipe-topic, and recipe-property
create_graph(df, 'recipe-viewer')
create_graph(df, 'recipe-topic')
create_graph(df, 'recipe-property')
