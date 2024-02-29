import matplotlib.pyplot as plt
import numpy as np

# This is an example of a matrix, not the real data...

support_channels = ["Community Calls", "Slack", "Mailing List", "Robert Sanderson"]
tools_resources = ["Documentation", "GitHub", "Workshops", "Reference Materials"]

frequency_matrix = np.array([
    [8, 5, 6, 3],
    [6, 3, 2, 1],
    [2, 1, 4, 3],
    [4, 2, 3, 7]
])

fig, ax = plt.subplots()
im = ax.imshow(frequency_matrix, cmap='Blues')

# Set x-axis labels
ax.set_xticks(np.arange(len(tools_resources)))
ax.set_xticklabels(tools_resources, rotation=45, ha='right')

# Set y-axis labels
ax.set_yticks(np.arange(len(support_channels)))
ax.set_yticklabels(support_channels)

# Set the colorbar
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel("Frequency", rotation=-90, va="bottom")

# Add value annotations
for i in range(len(support_channels)):
    for j in range(len(tools_resources)):
        text = ax.text(j, i, frequency_matrix[i, j], ha='center', va='center', color='black')

# Adjust figure layout to prevent labels from being cut off
plt.tight_layout()

# Save the figure as SVG and PDF
plt.savefig("linkedart_practices.svg")
plt.savefig("linkedart_practices.pdf")

# Show the figure
plt.show()
