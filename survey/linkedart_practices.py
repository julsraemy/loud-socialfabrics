import numpy as np
import matplotlib.pyplot as plt

# Define the data
support_channels = ["Community Calls", "Slack", "Mailing List", "GitHub Issues", "Direct Communication (Robert Sanderson)", "Workshops"]
tools_reference = ["Documentation", "GitHub Issues", "Tools and Reference Materials", "Collaboration (Sharing Experiences, Posting Messages, etc.)"]

# Define the frequency matrix
frequency_matrix = np.array([
    [5, 0, 0, 0],
    [1, 2, 3, 0],
    [0, 0, 0, 0],
    [0, 6, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 1]
])

# Set up the figure and axes
fig, ax = plt.subplots(figsize=(8, 6))

# Create the heatmap
heatmap = ax.imshow(frequency_matrix, cmap="Blues")

# Set the tick labels and positions
ax.set_xticks(np.arange(len(tools_reference)))
ax.set_yticks(np.arange(len(support_channels)))
ax.set_xticklabels(tools_reference, rotation=45, ha="right")
ax.set_yticklabels(support_channels)

# Loop over the data and create text annotations
for i in range(len(support_channels)):
    for j in range(len(tools_reference)):
        text = ax.text(j, i, frequency_matrix[i, j], ha="center", va="center", color="black", fontsize=9)

# Set the colorbar
cbar = plt.colorbar(heatmap)
cbar.set_label("Frequency", rotation=90)

# Set the title and axis labels
plt.title("Support Channels for Linked Art Challenges and Tools and Reference Materials")
plt.xlabel("Tools and Reference Materials")
plt.ylabel("Support Channels")

# Save the figure as SVG and PDF
plt.savefig("heatmap.svg", format="svg")
plt.savefig("heatmap.pdf", format="pdf")

# Show the heatmap
plt.show()
