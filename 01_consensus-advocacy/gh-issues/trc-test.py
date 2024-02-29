import requests
import csv

# Set your personal access token here
personal_access_token = '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'

# Set the GitHub repository details
owner = 'IIIF'
repo = 'trc'

# Set the base URL for GitHub API
base_url = f'https://api.github.com/repos/{owner}/{repo}'

# Set the headers for authentication
headers = {
    'Authorization': f'Token {personal_access_token}'
}

# Make API request to get repository information
repo_data = requests.get(base_url, headers=headers).json()

# Extract repository information
repo_name = repo_data['name']
open_issues = repo_data['open_issues']
total_issues = repo_data['open_issues_count']

# Make API request to get issues information with pagination
issues_url = f'{base_url}/issues?state=all'
issues_data = []
while issues_url:
    issues_response = requests.get(issues_url, headers=headers)
    issues_data += issues_response.json()
    issues_url = issues_response.links.get('next', {}).get('url')

# Open a CSV file for writing
with open('trc_issues.csv', 'w', newline='') as csvfile:
    fieldnames = ['Issue Number', 'Title', 'Created At', 'Closed At', 'Commenter', 'Reaction Type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through the issues data and write to CSV
    for issue in issues_data:
        issue_number = issue['number']
        title = issue['title']
        created_at = issue['created_at']
        closed_at = issue['closed_at']
        commenter = ''
        reaction_type = ''

        # Check if the issue is closed
        if closed_at:
            # Make API request to get comments for the closed issue
            comments_url = f'{base_url}/issues/{issue_number}/comments'
            comments_data = []
            while comments_url:
                comments_response = requests.get(comments_url, headers=headers)
                comments_data += comments_response.json()
                comments_url = comments_response.links.get('next', {}).get('url')

            # Iterate through the comments data and extract commenter and reaction type
            for comment in comments_data:
                commenter = comment['user']['login']
                reactions = comment['reactions']
                if reactions['total_count'] > 0:
                    reaction_type = reactions['url']
                    break

        # Write the issue data to CSV
        writer.writerow({
            'Issue Number': issue_number,
            'Title': title,
            'Created At': created_at,
            'Closed At': closed_at,
            'Commenter': commenter,
            'Reaction Type': reaction_type
        })

print('CSV file with GitHub issues data has been created successfully.')
