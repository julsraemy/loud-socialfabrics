import pandas as pd

# Assuming you have the data in a CSV file named 'heatmap.csv'
df = pd.read_csv('heatmap.csv')

# Get the column containing IIIF event attendance information
attendance_column = df.iloc[:, 9]  # Assuming the column index is 9 (10th column)

# Define the possible answers
possible_answers = [
    'IIIF Annual Conference',
    'IIIF Online Meeting (previouslyFall Working Meeting)',
    'IIIF Online Workshop/Training',
    'IIIF Hackathon',
    'A formal ad-hoc IIIF Meeting to focus on and develop the specifications (e.g. APIs, extensions)',
    'A regional/informal IIIF Event (not necessarily organised by the IIIF-Consortium)'
]

# Iterate over each row and update the values in the column
for i, event in enumerate(attendance_column):
    if event in possible_answers:
        attendance_column[i] = f"{event}: {attendance_column.value_counts()[event]}"

# Save the modified DataFrame back to the CSV file
df.to_csv('heatmap_modified.csv', index=False)
