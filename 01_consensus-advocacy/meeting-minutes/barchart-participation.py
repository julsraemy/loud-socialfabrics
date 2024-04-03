import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_stacked_bar_chart(csv_path, output_file_base, total_meetings, date_range):
    # Load the dataset
    df = pd.read_csv(csv_path)

    # Filtering relevant columns and sorting by total attendance
    df = df.filter(regex='name|present_total|present_20')
    df.sort_values(by='present_total', ascending=False, inplace=True)

    # Calculating additional stats
    avg_attendance = df['present_total'].mean()
    median_attendance = df['present_total'].median()
    num_unique_participants = df['name'].nunique()

    # Preparing data for plotting
    plot_data = df.drop(columns=['present_total']).set_index('name')

    # Setting up the figure for plotting
    plt.figure(figsize=(14, 10))

    # Determining the color palette based on the dataset
    num_years = len(plot_data.columns)
    cmap = plt.get_cmap('Purples') if 'la_data' in csv_path else plt.get_cmap('Blues')
    colors = cmap(np.linspace(0.5, 1, num_years))

    # Creating the stacked bar plot
    for i, column in enumerate(plot_data.columns):
        year = column.split('_')[-1]  # Extracting the year from the column name
        plt.barh(plot_data.index, plot_data[column], left=plot_data[plot_data.columns[:i]].sum(axis=1),
                 color=colors[i], label=year if i < num_years else "")

    # Annotating the chart with calculated and provided stats
    annotation_text = (f'Unique Participants: {num_unique_participants}\n'
                       f'Total Meetings ({date_range}): {total_meetings}\n'
                       f'Average Attendance per Participant: {avg_attendance:.2f}\n'
                       f'Median Attendance per Participant: {median_attendance}')
    plt.text(0.98, 0.95, annotation_text,
             verticalalignment='top', horizontalalignment='right',
             transform=plt.gca().transAxes,
             color='green', fontsize=12)

    # Adjusting legend, labels, and layout
    plt.xlabel('Number of Meetings Attended')
    plt.legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.yticks([])  # Optionally hiding participant names for clarity

    plt.tight_layout()

    # Save the figure in both PDF and SVG formats
    plt.savefig(f"{output_file_base}.pdf")
    plt.savefig(f"{output_file_base}.svg")

    plt.close()

# Dataset paths, output base paths (without file extension), and specific data for annotations
datasets_info = {
    './la_data/aggregated_person_data.csv': ('./la_data/attendance_stacked_bar', 115, 'January 2019 - March 2024'),
    './tsg_data/aggregated_person_data.csv': ('./tsg_data/attendance_stacked_bar', 101, 'February 2017 - March 2023')
}

# Generate the bar charts with additional annotations
for csv_path, (output_file_base, total_meetings, date_range) in datasets_info.items():
    create_stacked_bar_chart(csv_path, output_file_base, total_meetings, date_range)

print("The stacked bar charts with enhanced annotations have been generated and saved in both PDF and SVG formats.")
