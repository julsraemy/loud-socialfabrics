# Meeting Minutes

## Overview

I extracted the meeting minutes of the IIIF Discovery Technical Specification Group, covering the period from December 2017 to March 2023, as well as the Linked Art Community minutes from January 2019 to March 2024. These documents were originally stored in Google Docs. To facilitate this process, I used a dedicated tool developed by [the Gift of Script](https://www.pbainbridge.co.uk/), created by Phil Bainbridge. This tool was able to efficiently extract key information from the documents, including file names, direct links to files, and paragraph content, streamlining access to and analysis of these valuable resources. The extracted data was organised and saved as CSV files, which are available in the [raw](raw/) directory.

## Data Cleaning

Once extracted, the CSV files underwent a cleaning process to ensure that the data was accurate and correctly formatted for analysis, in particular using OpenRefine to correct inconsistencies, remove duplicates and ensure the overall quality of the data. The cleaned or amended versions of the CSV files are used as the basis for further processing and analysis.

## Curation

The `meeting_minutes_curation.py` performs the following functions:

1. **Normalisation**: Standardises the format of the data across different sources, making it consistent and easier to analyze.
2. **Extraction of Key Information**: Identifies and extracts vital information from the cleaned data, such as names of participants, dates, and links mentioned during the meetings.
3. **Preparation for Aggregation**: Structures the data in a way that facilitates the aggregation phase.

This script must be executed first as it prepares the data for the subsequent aggregation process by organising and refining it into a structured format.

## Aggregated results

The `meeting_minutes_agg.py` script builds on the curated data to provide aggregated insights. This script completes the analysis by creating three CSV files which are aggregated views of the data in terms of hyperlinks (at domain level), participants and yearly statistics.