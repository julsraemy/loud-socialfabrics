import matplotlib.pyplot as plt

data = [
    (1, "IIIF Specifications", 0, 8),
    (2, "IIIF Presentation API Validator", 0, 8),
    (3, "IIIF Website", 0, 5),
    (4, "Resources from the Community and Technical Specification Groups", 1, 1),
    (5, "Universal Viewer", 2, 10),
    (6, "Exhibit", 3, 2),
    (7, "Storiiies", 3, 3),
    (8, "FromThePage", 3, 1),
    (9, "Mirador", 2, 13),
    (10, "OpenSeaDragon", 2, 1),
    (11, "IIIF Training", 1, 2),
    (12, "IIIF Cookbook", 1, 4),
    (13, "IIIF Awesome", 1, 3),
    (14, "Cropping Tool", 2, 1),
    (15, "Cantaloupe", 2, 5),
    (16, "IIIF GitHub", 1, 4),
    (17, "IIIF Slack workspace", 0, 4),
    (18, "Tify", 2, 1),
    (19, "Annonatate", 2, 1),
    (20, "SimpleAnnotationServer", 2, 3),
    (21, "Wax", 2, 2),
    (22, "IIIF-Discuss", 0, 1),
    (23, "Viewers", None, 5),
    (24, "CanvasPanel", 1, 1),
    (25, "IIIF Google Drive", 0, 2),
    (26, "Annotation Services", None, 1),
    (27, "IIIF YouTube Channel", 0, 1),
    (28, "Custom libraries", None, 1),
    (29, "Custom UI Components", None, 1),
    (30, "PyIIIFpres", 2, 1),
    (31, "iiif-prezi3", 1, 1),
    (32, "IIIF Newsletter", 0, 1),
    (33, "Bodleian Manifest Editor", 2, 1),
    (34, "iiif-training-workbench", 2, 1),
    (35, "IIIF Curation Platform", 3, 1),
    (36, "Servers", None, 1),
    (37, "Biblissima", 3, 1),
    (38, "IIIF-Metadatahandboek", 3, 1),
    (39, "IIIFHosting", 3, 1),
    (40, "Annona", 2, 1),
    (41, "IIIF-related Omeka modules", 2, 1),
    (42, "Miiify", 2, 1),
    (43, "Loris", 2, 1),
    (44, "go-iiif", 0, 1),
    (45, "annotorious", 2, 1),
    (46, "solr-ocrhighlighting (DBMDZ)", 2, 1),
    (47, "IIPImage", 2, 1),
    (48, "IIIF Image API Validator", 0, 1),
    (49, "Open Access Tools", 2, 1),
]

# Filter out data points with N/A position
filtered_data = [(id_, tool, position, frequency) for id_, tool, position, frequency in data if position is not None]

# Group data points with the same coordinates
grouped_data = {}
for id_, tool, position, frequency in filtered_data:
    if (position, frequency) in grouped_data:
        grouped_data[(position, frequency)].append((id_, tool))
    else:
        grouped_data[(position, frequency)] = [(id_, tool)]

# Extract x and y coordinates
x = [position for position, frequency in grouped_data.keys()]
y = [frequency for position, frequency in grouped_data.keys()]

# Set up plot
plt.scatter(x, y, s=80, c='blue')
plt.xlabel("Position")
plt.ylabel("Frequency")
plt.title("Tools/Services Used in IIIF Community")
plt.xticks(range(4), labels=["0", "1", "2", "3"])
plt.ylim(0, 13)

# Add labels to each point
for i, (position, frequency) in enumerate(grouped_data.keys()):
    labels = [str(id_) for id_, tool in grouped_data[(position, frequency)]]
    offset = (i - len(labels) / 2 + 0.5) * 0.2  # Offset for labels with same coordinates
    for j, label in enumerate(labels):
        plt.annotate(label, (position, frequency), textcoords="offset points", xytext=(offset, 10), ha='center', fontsize=8)

# Highlight N/A positions
na_indices = [i for i, position in enumerate(x) if position is None]
for index in na_indices:
    plt.scatter(None, y[index], s=80, c='lightgray')

# Create legend
legend_labels = []
for tool_group in grouped_data.values():
    labels = [str(id_) for id_ in [tool_group[0]]]
    legend_labels.append(", ".join(labels))
legend_labels.append("N/A")
plt.legend(legend_labels, loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3)

# Save plot as SVG and PDF
plt.grid(True)
plt.savefig("iiif_tools_services.svg", format="svg")
plt.savefig("iiif_tools_services.pdf", format="pdf")
