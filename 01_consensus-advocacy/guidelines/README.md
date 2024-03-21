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

### JSON Structure and Path Analysis

**File:** [01b_iiif-recipes-json-paths.py](./01b_iiif-recipes-json-paths.py)

Analyzes the JSON structure of the IIIF Cookbook recipes to identify and count common JSON paths and content links, with results available in both CSV and Markdown formats.

### Content Similarity Among Recipes

**File:** [01c_iiif-recipes-json-similarity.py](./01c_iiif-recipes-json-similarity.py)

Compares content similarity across IIIF Cookbook recipes based on their JSON structures, leveraging cosine similarity metrics for analysis, suitable for graph-based visualization and analysis tools.

## Linked Art Patterns (Model Components)

TBD
