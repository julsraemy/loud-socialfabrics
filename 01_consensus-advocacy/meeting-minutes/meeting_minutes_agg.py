import pandas as pd
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

def initialize_years(df):
    years = sorted(set(df['date'].str.slice(0, 4)))
    return years

def aggregate_person_data(df, years):
    person_data = defaultdict(lambda: {f'present_{year}': 0 for year in years} | {f'regrets_{year}': 0 for year in years})
    for _, row in df.iterrows():
        year = row['date'][:4]
        for name in str(row['present']).split(';'):
            if name:
                person_data[name][f'present_{year}'] += 1
        for name in str(row['regrets']).split(';'):
            if name:
                person_data[name][f'regrets_{year}'] += 1
    return person_data

def aggregate_domain_data(df, years):
    domain_data = defaultdict(lambda: {f'mention_{year}': 0 for year in years})
    for _, row in df.iterrows():
        year = row['date'][:4]
        links = str(row['links']).split(';')
        for link in links:
            if link:
                domain = urlparse(link).netloc
                domain_data[domain][f'mention_{year}'] += 1
    return domain_data

def save_aggregated_data(person_data, domain_data, years, output_dir):
    person_cols = ['name'] + [f'present_{year}' for year in years] + [f'regrets_{year}' for year in years]
    domain_cols = ['name'] + [f'mention_{year}' for year in years]

    person_rows = [{**{'name': name}, **data} for name, data in person_data.items()]
    domain_rows = [{**{'name': domain}, **data} for domain, data in domain_data.items()]

    person_df = pd.DataFrame(person_rows, columns=person_cols)
    domain_df = pd.DataFrame(domain_rows, columns=domain_cols)

    person_df.to_csv(Path(output_dir) / "aggregated_person_data.csv", index=False)
    domain_df.to_csv(Path(output_dir) / "aggregated_domain_data.csv", index=False)

def process_dataset(csv_path, output_dir):
    df = pd.read_csv(csv_path)
    years = initialize_years(df)
    person_data = aggregate_person_data(df, years)
    domain_data = aggregate_domain_data(df, years)
    save_aggregated_data(person_data, domain_data, years, output_dir)

def main():
    tsg_path = Path(__file__).parent / "tsg_data" / "tsg_extended.csv"
    la_path = Path(__file__).parent / "la_data" / "la_extended.csv"

    process_dataset(tsg_path, tsg_path.parent)
    process_dataset(la_path, la_path.parent)

if __name__ == "__main__":
    main()
