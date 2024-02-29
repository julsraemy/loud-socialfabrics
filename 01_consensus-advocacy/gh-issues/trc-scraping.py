import requests
import csv

# GitHub repository detail
repo_owner = 'IIIF'
repo_name = 'trc'

# Make a request to the GitHub API to get the total number of issues in the repository
repo_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}'
repo_response = requests.get(repo_url)
repo_data = repo_response.json()
total_issues = repo_data['open_issues']

# Define the base URL for issues API with pagination
base_issues_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues?per_page=100&page='

# Initialize the list to store all issues data
all_issues_data = []

# Loop through all pages of issues data
for page in range(1, (total_issues // 100) + 2):
    # Make a request to the GitHub API to get issues data for the current page
    issues_url = base_issues_url + str(page)
    issues_response = requests.get(issues_url)

    # Check if the request was successful
    if issues_response.status_code == 200:
        # Parse the issues data from the response JSON
        issues_data = issues_response.json()

        # Loop through each issue in the issues data
        for issue in issues_data:
            # Get issue details
            issue_number = issue['number']
            issue_title = issue['title']
            issue_state = issue['state']
            issue_created_at = issue['created_at']
            issue_closed_at = issue['closed_at']

            # Initialize counters for comments and reactions
            num_comments = 0
            reactions = {'+1': 0, '-1': 0, 'laugh': 0, 'confused': 0, 'heart': 0, 'hooray': 0}

            # Check if the issue is closed
            if issue_state == 'closed':
                # Get the comments data for the closed issue
                comments_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/comments'
                comments_response = requests.get(comments_url)

                # Check if the request was successful
                if comments_response.status_code == 200:
                    # Parse the comments data from the response JSON
                    comments_data = comments_response.json()

                    # Loop through each comment in the comments data
                    for comment in comments_data:
                        # Get commenter details
                        commenter = comment['user']['login']
                        num_comments += 1

                        # Get reaction details
                        for reaction in comment['reactions']['nodes']:
                            reaction_type = reaction['content']
                            reactions[reaction_type] += 1

            # Get contributor details
            contributors_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/assignees'
            contributors_response = requests.get(contributors_url)

            # Check if the request was successful
            if contributors_response.status_code == 200:
                # Parse the contributors data from the response JSON
                contributors_data = contributors_response.json()

                # Get the usernames of the contributors
                contributors = [contributor['login'] for contributor in contributors_data]

            # Append the issue data to the list of all issues data
            all_issues_data.append([issue_number, issue_title, issue_state, issue_created_at, issue_closed_at, num_comments,
                                     reactions['+1'], reactions['-1'], reactions['laugh'], reactions['confused'],
                                     reactions['heart'], reactions['hooray'], ','.join(contributors)])

# Write the all issues data to a CSV file
csv_file = 'github_issues.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Issue Number', 'Title', 'State', 'Created At', 'Closed At', 'Num Comments', '+1 Reactions',
                     '-1 Reactions', 'Laugh Reactions', 'Confused Reactions', 'Heart Reactions', 'Hooray Reactions',
                     'Contributors'])
    writer.writerows(all_issues_data)

print(f'Saved data to {csv_file} successfully!')
