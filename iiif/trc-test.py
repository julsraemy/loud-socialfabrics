import requests
import csv

# Set the repository owner and name
repo_owner = 'IIIF'
repo_name = 'trc'

# Make a request to the GitHub API to get the issues data
url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues?state=all'
response = requests.get(url)

# Check if the request was successful
if response.status_code != 200:
    print('Error: Could not retrieve issue data')
    exit()

# Parse the issues data from the response JSON
issues_data = response.json()

# Create a CSV file to store the issue data
with open('trc-data.csv', 'w', newline='') as csvfile:
    # Define the CSV writer
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['Issue Number', 'Title', 'State', 'Number of Comments', 'Contributors', 'Reactions'])

    # Loop through each issue and write its data to the CSV
    for issue in issues_data:
        issue_number = issue['number']
        title = issue['title']
        state = issue['state']
        num_comments = issue['comments']
        
        # Get the names of contributors who commented on the issue
        contributors = []
        for comment in issue['comments_url']:
            if 'user' in comment and 'login' in comment['user']:
                commenter = comment['user']['login']
                if commenter not in contributors:
                    contributors.append(commenter)
        
        # Get the reactions for the issue
        reactions = {}
        for reaction in issue['reactions']:
            if 'content' in reaction:
                reaction_type = reaction['content']
                if reaction_type in reactions:
                    reactions[reaction_type] += 1
                else:
                    reactions[reaction_type] = 1
        
        # Write the issue data to the CSV file
        writer.writerow([issue_number, title, state, num_comments, ', '.join(contributors), reactions])
