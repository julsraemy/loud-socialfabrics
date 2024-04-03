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

## Aggregated Results

The `meeting_minutes_agg.py` script builds on the curated data to provide aggregated insights. This script completes the analysis by creating three CSV files which are aggregated views of the data in terms of hyperlinks (at domain level), participants and yearly statistics.

## Stacked Bar Charts Showing Meeting Attendance

To visually represent participation in meetings over time, stacked bar graphs were created for both the IIIF Discovery Technical Specification Group and the Linked Art Community meetings. These charts highlight the attendance for each meeting and break down the attendance by year to show trends and changes in engagement.

Building on this aggregated data, another script, `barchart-participation.py`, has been developed to perform the following key tasks:

1. **Data preparation**: Extracts and organises the attendance data from the aggregated CSV files, focusing on total attendance per attendee and attendance per year.
2. **Colour Scheme Selection**: Assigns different colour schemes to each dataset for visual differentiation. Shades of purple are used for the Linked Art community, while shades of blue represent the IIIF TSG meetings.
3. **Statistical Annotations**: In addition to visualising participation, the script calculates and annotates each graph with valuable statistics, including
   - The average attendance per attendee.
   - The median attendance, highlighting the central tendency of attendance.
   - The total number of sessions and the time period they cover.
   - The number of unique attendees, providing insight into the size and engagement of the community.
4. **Outputs**: Charts are saved in both PDF and SVG formats.

## Topic Modelling

TBD