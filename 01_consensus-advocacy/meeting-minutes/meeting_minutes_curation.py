import pandas as pd
import re
from pathlib import Path
from nltk.tokenize import sent_tokenize

def clean_names(names_str):
    """Clean and process names, excluding content within parentheses for each name."""
    if pd.isna(names_str):
        return '', 0
    # Splitting on commas to process each name individually
    names_parts = names_str.split(',')
    cleaned_names = []
    for part in names_parts:
        # Exclude content within parentheses for each part/name
        name_cleaned = re.sub(r'\s*\(.*?\)', '', part).strip()
        # Add the cleaned name if it's not empty
        if name_cleaned:
            cleaned_names.append(name_cleaned)
    return ';'.join(cleaned_names), len(cleaned_names)

def clean_links(links_str):
    """Clean links by removing unwanted URLs and trailing characters."""
    if pd.isna(links_str):
        return ''
    links = re.findall(r'https?://[^\s,\]]+', links_str)
    cleaned_links = [re.sub(r'\)$', '', link) for link in links if 'zoom.us' not in link and 'bluejeans.com' not in link and 'bit.ly/linked_art_call' not in link]
    return ';'.join(cleaned_links)

def generate_summary(content):
    """Generate a coherent paragraph summary of the content, with a limit of 500 words."""
    if pd.isna(content):
        return ''
    sentences = sent_tokenize(content)
    summary_sentences = sentences[:min(len(sentences), 20)]  # Pick top sentences for brevity
    summary = ' '.join(summary_sentences)
    words = summary.split()
    return ' '.join(words[:500])  # Limit to 500 words

def process_and_save_data(input_path, data_dir_name, output_filename):
    df = pd.read_csv(input_path)
    df['present'], df['present_count'] = zip(*df['present'].apply(clean_names))
    df['regrets'], df['regrets_count'] = zip(*df['regrets'].apply(clean_names))
    df['links'] = df['links'].apply(clean_links)
    df['summary'] = df['content'].apply(generate_summary)
    df.drop('topics', axis=1, inplace=True, errors='ignore')

    output_path = Path(__file__).parent / data_dir_name / output_filename
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False)

# Paths to the cleaned CSV files
tsg_path = Path(__file__).parent / "amended_iiif_discovery_tsg.csv"
la_path = Path(__file__).parent / "amended_linked-art_meetings.csv"

# Process and save the extended CSVs
process_and_save_data(tsg_path, "tsg_data", "tsg_extended.csv")
process_and_save_data(la_path, "la_data", "la_extended.csv")
