import pandas as pd
from collections import defaultdict, Counter
from pathlib import Path
from urllib.parse import urlparse

def process_names(names_str):
    if pd.isna(names_str):
        return []
    return [name.strip().split('(')[0] for name in names_str.split(';') if name.strip()]

def extract_domains(links_str):
    if pd.isna(links_str):
        return []
    return [urlparse(link.strip()).netloc for link in links_str.split(';') if link.strip() and not any(excluded in link for excluded in ["zoom.us", "bluejeans.com", "bit.ly/linked_art_call"])]

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def aggregate_person_data(df, years):
    person_data = defaultdict(lambda: {'present_total': 0, 'regrets_total': 0, **{f'present_{year}': 0 for year in years}, **{f'regrets_{year}': 0 for year in years}})
    for _, row in df.iterrows():
        year = row['date'][:4]
        for name in process_names(row['present']):
            person_data[name][f'present_{year}'] += 1
            person_data[name]['present_total'] += 1
        for name in process_names(row['regrets']):
            person_data[name][f'regrets_{year}'] += 1
            person_data[name]['regrets_total'] += 1
    return dict(person_data)

def aggregate_domain_data(df, years):
    domain_data = defaultdict(lambda: {'mention_total': 0, **{f'mention_{year}': 0 for year in years}})
    for _, row in df.iterrows():
        year = row['date'][:4]
        for domain in extract_domains(row['links']):
            domain_data[domain][f'mention_{year}'] += 1
            domain_data[domain]['mention_total'] += 1
    return dict(domain_data)

def aggregate_yearly_meeting_data(df):
    yearly_data = defaultdict(lambda: {'total_meetings': 0, 'participants': set(), 'total_present': 0})
    for _, row in df.iterrows():
        year = row['date'][:4]
        yearly_data[year]['total_meetings'] += 1
        present_names = process_names(row['present'])
        yearly_data[year]['participants'].update(present_names)
        yearly_data[year]['total_present'] += len(present_names)
    for year in yearly_data:
        yearly_data[year]['total_unique_participants'] = len(yearly_data[year]['participants'])
        if yearly_data[year]['total_meetings'] > 0:
            yearly_data[year]['average_present'] = round(yearly_data[year]['total_present'] / yearly_data[year]['total_meetings'], 2)
        else:
            yearly_data[year]['average_present'] = 0
        yearly_data[year]['participants'] = '; '.join(yearly_data[year]['participants'])
    return dict(yearly_data)

# Ensure the rest of the script is unchanged and integrates this adjusted function as before.

def save_aggregated_data(person_data, domain_data, yearly_meeting_data, output_dir, years):
    person_df = pd.DataFrame.from_dict(person_data, orient='index', columns=['present_total', 'regrets_total'] + [f'{term}_{year}' for year in years for term in ('present', 'regrets')]).reset_index().rename(columns={'index': 'name'})
    domain_df = pd.DataFrame.from_dict(domain_data, orient='index', columns=['mention_total'] + [f'mention_{year}' for year in years]).reset_index().rename(columns={'index': 'name'})
    yearly_df = pd.DataFrame.from_dict(yearly_meeting_data, orient='index', columns=['total_meetings', 'total_unique_participants', 'average_present', 'participants']).reset_index().rename(columns={'index': 'year'})
    
    person_df.to_csv(Path(output_dir) / "aggregated_person_data.csv", index=False)
    domain_df.to_csv(Path(output_dir) / "aggregated_domain_data.csv", index=False)
    yearly_df.to_csv(Path(output_dir) / "aggregated_yearly_meetings.csv", index=False)


def process_dataset(csv_path, output_dir):
    df = load_data(csv_path)
    years = sorted(set(df['date'].str.slice(0, 4)))
    person_data = aggregate_person_data(df, years)
    domain_data = aggregate_domain_data(df, years)
    yearly_meeting_data = aggregate_yearly_meeting_data(df)
    save_aggregated_data(person_data, domain_data, yearly_meeting_data, output_dir, years)

def main():
    process_dataset(Path(__file__).parent / "tsg_data" / "tsg_extended.csv", Path(__file__).parent / "tsg_data")
    process_dataset(Path(__file__).parent / "la_data" / "la_extended.csv", Path(__file__).parent / "la_data")

if __name__ == "__main__":
    main()
