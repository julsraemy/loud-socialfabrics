import requests
from bs4 import BeautifulSoup
import csv
import re

# Fetch the organization page and parse the HTML
org_name = 'IIIF'
url = f'https://github.com/{org_name}'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the repository names from the HTML
repo_names = []
for repo_link in soup.find_all('a', {'itemprop': 'name codeRepository'}):
    repo_names.append(repo_link['href'].split('/')[-1])

# Initialize the CSV output file
with open('iiif_github_stats.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(['Repository', 'Number of Issues', 'Number of Pull Requests', 'Contributors', 'Reactions'])

    # Loop through each repository and scrape the desired information
    for repo_name in repo_names:
        print(f'Scraping repository: {repo_name}')

        # Fetch the repository page and parse the HTML
        url = f'https://github.com/{org_name}/{repo_name}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the number of issues and pull requests
        issue_count_text = soup.find('a', {'href': f'/{org_name}/{repo_name}/issues'}).text.strip()
        issue_count = int(re.search(r"\d+", issue_count_text).group())
        pr_count_text = soup.find('a', {'href': f'/{org_name}/{repo_name}/pulls'}).text.strip().replace(',', '')
        pr_count = int(re.search(r'\d+', pr_count_text).group())

        # Extract the contributors
        contributors = set()
        for contributor in soup.find_all('a', {'data-hovercard-type': 'user'}):
            contributors.add(contributor.text.strip())
        contributor_count = len(contributors)

        # Extract the reactions on issues and pull requests
        reaction_count = 0
        for issue_link in soup.find_all('a', {'href': f'/{org_name}/{repo_name}/issues'}):
            issue_url = f"https://github.com{issue_link['href']}"
            issue_response = requests.get(issue_url)
            issue_soup = BeautifulSoup(issue_response.text, 'html.parser')
            for reaction_tag in issue_soup.find_all('reaction-summary-item'):
                reaction_count += int(re.findall(r'\d+', reaction_tag.text)[0])

        for pr_link in soup.find_all('a', {'href': f'/{org_name}/{repo_name}/pulls'}):
            pr_url = f"https://github.com{pr_link['href']}"
            pr_response = requests.get(pr_url)
            pr_soup = BeautifulSoup(pr_response.text, 'html.parser')
            for reaction_tag in pr_soup.find_all('reaction-summary-item'):
                reaction_count += int(re.findall(r'\d+', reaction_tag.text)[0])

        # Write the results to the CSV file
        writer.writerow([repo_name, issue_count, pr_count, contributor_count, reaction_count])