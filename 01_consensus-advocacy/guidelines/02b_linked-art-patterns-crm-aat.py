import pandas as pd
import requests
import networkx as nx
import os
import csv
from collections import Counter

def fetch_json(url):
    """Fetch JSON data from a URL."""
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def process_json(json_data):
    """Extract relevant data from JSON."""
    aat_terms = set()
    main_type = json_data.get('type', 'Unknown') if json_data else 'Unknown'
    if json_data:
        for classified in json_data.get('classified_as', []):
            if 'http://vocab.getty.edu/aat/' in classified.get('id', ''):
                aat_terms.add((classified.get('id'), classified.get('_label', 'Unknown')))
    return main_type, aat_terms

# Set up paths
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'patterns', 'linked_art_patterns.csv')
gexf_path = os.path.join(script_dir, 'patterns', 'linked_art_patterns_crm_aat.gexf')
md_path = os.path.join(script_dir, 'patterns', 'linked_art_patterns_crm_aat_statistics.md')
csv_stats_path = os.path.join(script_dir, 'patterns', 'linked_art_patterns_crm_aat_statistics.csv')

# Load CSV
df = pd.read_csv(csv_path)

# Initialize graph and statistics counters
G = nx.Graph()
aat_terms_counter = Counter()
main_types_counter = Counter()

# Process each row in the dataframe
for _, row in df.iterrows():
    json_urls = str(row['json']).split(';') if pd.notna(row['json']) else []
    pattern_label = f"{row['id']}: {row['pattern']}"
    G.add_node(pattern_label, type='Pattern')
    for json_url in json_urls:
        json_data = fetch_json(json_url.strip())
        main_type, aat_terms = process_json(json_data)
        
        # Add main type as a node
        if main_type != 'Unknown':
            G.add_node(main_type, type='CIDOC-CRM Type')
            G.add_edge(pattern_label, main_type)
        
        # Update graph with AAT terms
        for aat_id, aat_label in aat_terms:
            aat_node_label = f"{aat_label} ({aat_id})"
            G.add_node(aat_node_label, type='AAT Term')
            G.add_edge(pattern_label, aat_node_label)
            aat_terms_counter[aat_node_label] += 1
        
        main_types_counter[main_type] += 1

# Save graph to GEXF
nx.write_gexf(G, gexf_path)

# Save statistics to MD and CSV
with open(md_path, 'w') as f_md, open(csv_stats_path, 'w', newline='') as f_csv:
    writer = csv.writer(f_csv)
    writer.writerow(['Type', 'Label', 'Count'])

    # MD Content for AAT Terms and Main CRM/LA Classes
    f_md.write("# Linked Art Patterns Statistics\n\n## AAT Terms\n")
    for term, count in aat_terms_counter.most_common():
        aat_id, aat_label = term.split(' (')
        f_md.write(f"- {aat_label[:-1]}: {count} ({aat_id})\n")
        writer.writerow(['AAT Term', aat_label[:-1], count])

    f_md.write("\n## Main CRM/LA Class\n")
    for type_, count in main_types_counter.most_common():
        f_md.write(f"- {type_}: {count}\n")
        writer.writerow(['Main CRM/LA Class', type_, count])

print(f"Graph saved to: {gexf_path}")
print(f"Statistics saved to: {md_path} and {csv_stats_path}")
