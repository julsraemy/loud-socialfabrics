import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
data = pd.read_csv("heatmap.csv", dtype=str)

# Group the data by the IIIF and Linked Art columns and calculate the count
grouped_data = data.groupby(['How frequently have you taken part in a IIIF Community Call over the past year?',
                             'How frequently have you taken part in the bi-weekly Linked Art Call over the past year?']).size().unstack()

# Plotting the bar chart
fig, ax = plt.subplots(figsize=(10, 6))
grouped_data.plot(kind='bar', ax=ax)

# Set the chart title and labels
ax.set_title('Frequency of Participation in IIIF Community Calls and Linked Art Calls')
ax.set_xlabel('IIIF Community Call Frequency')
ax.set_ylabel('Count')

# Display the legend
ax.legend(title='Linked Art Call Frequency', bbox_to_anchor=(1, 1))

# Rotate the x-axis labels for better readability
plt.xticks(rotation=45)

# Save the chart as a PDF file
plt.savefig('chart.pdf', bbox_inches='tight')

# Save the chart as an SVG file
plt.savefig('chart.svg', format='svg', bbox_inches='tight')

# Show the plot
plt.show()
