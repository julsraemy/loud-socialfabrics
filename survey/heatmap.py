import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
data = pd.read_csv('/Users/julienraemy/Documents/GitHub/juls/loud-socialfabrics/survey/heatmap.csv', dtype={
    'ID': str,
    'In which community are you involved?': str,
    'Since when have you been involved in the IIIF community?': float,
    'How frequently have you taken part in a IIIF Community Call over the past year?': str,
    'How frequently have you taken part in a IIIF Community Group Call over the past year?': str,
    'How frequently have you taken part in a IIIF Technical Specification Group Call over the past year?': str,
    'How frequently have you taken part in a IIIF Committee Call over the past year?': str,
    'Since when have you been involved in the Linked Art community?': float,
    'How frequently have you taken part in the bi-weekly Linked Art Call over the past year?': str,
}, na_values=['']).fillna({'Since when have you been involved in the IIIF community?': 0})

# Create a column to indicate the participation type
data['Participation'] = data['In which community are you involved?'].apply(lambda x: 'Both' if x == 'both' else x)

# Create a color map for the scatter plot
color_map = {
    'Both': 'purple',
    'IIIF': 'red',
    'Linked Art': 'blue',
}

# Create a scatter plot of participants
plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    data['Since when have you been involved in the IIIF community?'],
    data.index,
    c=data['Participation'].map(color_map),
    s=data['How frequently have you taken part in a IIIF Community Call over the past year?'].map({
        'Never': 30,
        'Less than 5 times a year': 90,
        'Between 5 and 10 times a year': 180,
        'More than 10 times a year': 360
    }),
    alpha=0.7
)

# Add annotations for Linked Art participants
# plt.annotate('N/A', (2022, 53), ha='center', va='center')
# plt.annotate('N/A', (2022, 54), ha='center', va='center')

# Set plot title and labels
plt.title('IIIF Calls Engagement')
plt.xlabel('Year of involvement in the IIIF community')
plt.ylabel('Participant ID')

# Create a legend for the color map, excluding the 'Linked Art' label
legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=8)
                  for category, color in color_map.items() if category != 'Linked Art']
plt.legend(legend_handles, [category for category in color_map.keys() if category != 'Linked Art'], loc='upper left')

# Save the plot as a PDF and SVG file
plt.savefig('heatmap.pdf', format='pdf')
plt.savefig('heatmap.svg', format='svg')

# Show the plot (optional)
plt.show()
