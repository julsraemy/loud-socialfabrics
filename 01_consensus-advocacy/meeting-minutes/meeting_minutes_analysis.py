import pandas as pd
import re
from pathlib import Path
from collections import defaultdict

# Paths to the CSV files
tsg_path = Path(__file__).parent / "iiif_discovery_tsg.csv"
la_path = Path(__file__).parent / "linked-art_meetings.csv"

# Regular expressions
date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
github_link_pattern = re.compile(r'https://github\.com/([\w-]+)/([\w-]+)/issues/(\d+)')
name_patterns = {
    "Robert Sanderson": re.compile(r'Rob(ert)? Sanderson'),
    "Bree Midavaine": re.compile(r'Bree Midavaine'),
    "Richard Palmer": re.compile(r'Richard Palmer'),
    "John Smith": re.compile(r'John Smith'),
    "Julien Raemy": re.compile(r'Julien\s+(A\.\s+)?Raemy'),
    "Kevin Page": re.compile(r'Kevin Page'),
}

# Function to extract data from a CSV file
def process_csv(file_path):
    df = pd.read_csv(file_path)
    dates = df['File Name'].apply(lambda name: date_pattern.search(name).group() if date_pattern.search(name) else None)
    
    issue_counts, issue_dates = process_github_links(df)
    
    # Identifying names and participation
    participation = {name: [] for name in name_patterns.keys()}
    for index, row in df.iterrows():
        text = ' '.join(row.astype(str))
        for name, pattern in name_patterns.items():
            if pattern.search(text):
                date = dates.iloc[index]
                if date:
                    participation[name].append(date)

    return dates.dropna().unique().tolist(), issue_counts, issue_dates, participation

# Function to process GitHub links, counting occurrences and tracking dates
def process_github_links(df):
    issue_counts = defaultdict(int)
    issue_dates = defaultdict(list)
    
    for index, row in df.iterrows():
        date = row['File Name']
        found_date = date_pattern.search(date).group() if date_pattern.search(date) else None
        text = ' '.join(row.astype(str))
        links = github_link_pattern.findall(text)
        for link in links:
            issue_counts[link] += 1
            if found_date:
                issue_dates[link].append(found_date)
    
    return issue_counts, issue_dates

# Saving functions
def save_data_to_file(file_path, data, is_dict=False):
    with open(file_path, 'w') as file:
        if is_dict:
            for key, value in data.items():
                if isinstance(value, list):  # Handling list values
                    file.write(f"{key}: {', '.join(value)}\n")
                else:  # Handling non-list values, such as integers
                    file.write(f"{key}: {value}\n")
        else:
            for item in data:
                file.write(f"{item}\n")

# Example usage for TSG data
tsg_dates, tsg_issue_counts, tsg_issue_dates, tsg_participation = process_csv(tsg_path)
tsg_data_path = Path(__file__).parent / "tsg_data"
tsg_data_path.mkdir(exist_ok=True)

save_data_to_file(tsg_data_path / "tsg_dates.txt", tsg_dates)
save_data_to_file(tsg_data_path / "tsg_github_issues.txt", tsg_issue_counts, is_dict=True)
save_data_to_file(tsg_data_path / "tsg_participation.txt", tsg_participation, is_dict=True)

# Repeat for Linked Art data as needed
la_dates, la_issue_counts, la_issue_dates, la_participation = process_csv(la_path)
la_data_path = Path(__file__).parent / "la_data"
la_data_path.mkdir(exist_ok=True)

save_data_to_file(la_data_path / "la_dates.txt", la_dates)
save_data_to_file(la_data_path / "la_github_issues.txt", la_issue_counts, is_dict=True)
save_data_to_file(la_data_path / "la_participation.txt", la_participation, is_dict=True)
