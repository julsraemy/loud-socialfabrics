import csv
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Set up Google Drive API credentials
creds = Credentials.from_authorized_user_file('loud-social-fabrics-e0eac5ffd820.json', ['https://www.googleapis.com/auth/drive'])

# Create a service for the Google Drive API
drive_service = build('drive', 'v3', credentials=creds)

# Define the folder ID of the Google Drive folder containing the Google Docs
folder_id = '0B_Alni5J8UNITzlpYW1MdnFpSlU'

# Get the list of files in the Google Drive folder
query = f"parents = '{folder_id}' and mimeType = 'application/vnd.google-apps.document'"
results = drive_service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
files = results.get('files', [])

# Loop through each Google Doc and extract paragraphs
all_data = []
for file in files:
    doc_id = file['id']
    doc_name = file['name']
    doc = drive_service.files().export(fileId=doc_id, mimeType='text/plain').execute()
    paragraphs = doc.split('\n\n')  # Assumes paragraphs are separated by two line breaks

    # Append paragraphs to the all_data list
    data = [doc_name] + paragraphs  # Include the doc name as the first column
    all_data.append(data)

print('Finished extracting data from all Google Docs.')

# Write data to CSV file
output_file = 'output.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Document Name', 'Paragraph 1', 'Paragraph 2', 'Paragraph 3'])  # Add more columns for additional paragraphs
    writer.writerows(all_data)

print(f'Successfully wrote data to {output_file}.')