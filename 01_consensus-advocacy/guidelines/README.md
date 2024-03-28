# Guidelines

## IIIF Cookbook Recipes

The following Python scripts are designed to analyze and visualize relationships within the IIIF Cookbook recipes, enhancing understanding of viewers, support properties, JSON structures, and content similarities.

### Recipe Metadata Extraction

**File:** [01_iiif-recipes-fetch.py](./01_iiif-recipes-fetch.py)

Extracts metadata from IIIF Cookbook recipes, including viewers, support status, and properties, and saves this information in a CSV file for further analysis.

### Network Graphs of Recipe Relationships

**File:** [01a_iiif-recipes-networkx.py](./01a_iiif-recipes-networkx.py)

Generates static graphs using NetworkX to visualize relationships between recipes and viewers, highlighting support properties within the IIIF Cookbook.

### Interactive Recipe Visualization

**File:** [01a_iiif-recipes-PyVis.py](./01a_iiif-recipes-PyVis.py)

Creates interactive visualizations of IIIF Cookbook recipes using PyVis, allowing for dynamic exploration of recipe connections and viewer support.

### Data Preparation for Gephi Analysis

**File:** [01a_iiif-recipes-gephi.py](./01a_iiif-recipes-gephi.py)

Prepares and exports recipe relationship data in a Gephi-compatible format, facilitating in-depth network analysis and visualization with external tools.

Amended GEFX file on Gist: https://gist.github.com/julsraemy/5fda62f3516e390a1203c9560574fbb4

### JSON Structure and Path Analysis

**File:** [01b_iiif-recipes-json-paths.py](./01b_iiif-recipes-json-paths.py)

Analyzes the JSON structure of the IIIF Cookbook recipes to identify and count common JSON paths and content links, with results available in both CSV and Markdown formats.

### Content Similarity Among Recipes

**File:** [01c_iiif-recipes-json-similarity.py](./01c_iiif-recipes-json-similarity.py)

Compares content similarity across IIIF Cookbook recipes based on their JSON structures, leveraging cosine similarity metrics for analysis, suitable for graph-based visualization and analysis tools.

## Linked Art Patterns (Model Components)

### Data Preparation for Gephi Analysis

**File:** [02a_linked-art-patterns-gephi.py](./02a_linked-art-patterns-gephi.py)

This script prepares and exports Linked Art pattern data in a Gephi-compatible format. It enables network analysis and visualization by creating a graph where nodes represent patterns and edges depict relationships derived from the patterns' data. 

Amended GEFX file on Gist: https://gist.github.com/julsraemy/db3ffc50e46a36da629b58e55f5f6f64

### CRM Classes and AAT Terms Analysis

**File:** [02b_linked-art-patterns-crm-aat.py](./02b_linked-art-patterns-crm-aat.py)

Analyzes and extracts CIDOC CRM Classes and AAT Terms from the Linked Art patterns' JSON data. It generates a network graph highlighting the connections between patterns based on their shared classes and terms.

Amended GEFX file on Gist: https://gist.github.com/julsraemy/f096c8e91b553c39240db1bef319bffd

### Content Similarity Among Linked Art Patterns

**File:** [02c_linked-art-patterns-json-similarity.py](./02c_linked-art-patterns-json-similarity.py)

Computes and visualizes content similarity among Linked Art patterns based on their JSON representations. The script evaluates textual and structural similarities, presenting the findings in a GEXF graph and detailed reports for further analysis.

# Remarks

In the exploration of [IIIF Cookbook Recipes](https://iiif.io/api/cookbook/) and [Linked Art Patterns](https://linked.art/model/), a comprehensive analysis was conducted through a series of Python scripts aimed at generating GEXF files for network analysis and content similarity assessment. These scripts serve as both a practical tool for data manipulation and a foundational codebase for further research and development. It's crucial to note, however, that not all generated GEXF files are equally suitable for direct visualization purposes.

While each GEXF file contributes to the broader understanding of data relationships and pattern recognitions within Linked Art and IIIF, practical application reveals that only a subset of these files demonstrate significant value when subjected to network visualization tools like Gephi. These particularly insightful GEXF files have been meticulously curated and are available for further examination through links to their respective Gists.
