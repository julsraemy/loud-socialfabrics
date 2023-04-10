import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set the URL for the repository
url = 'https://github.com/IIIF/trc'

# Send a GET request to the URL and get the response
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content of the response
soup = BeautifulSoup(response.content, 'html.parser')

# Find the section of the page with the issues
issues_section = soup.find('div', {'id': 'issues'})

# Find all the issue cards in the issues section
issue_cards = issues_section.find_all('div', {'class': 'Box-row--focus-gray'})

# Initialize lists to hold the data we want to scrape
open_closed = []
comments = []
contributors = []
reactions = []

# Loop through each issue card
for card in issue_cards:
    # Get the title of the issue
    title = card.find('a', {'class': 'Link--primary'}).text.strip()
    
    # Get the status of the issue (open or closed)
    status = card.find('span', {'class': 'State'}).text.strip()
    
    # Get the number of comments on the issue
    comment_count = card.find('span', {'class': 'Link--primary'}).text.strip()
    
    # Get the names of the contributors to the issue
    contributors_list = card.find('span', {'class': 'AvatarStack-body'}).find_all('a')
    contributor_names = [contributor.text.strip() for contributor in contributors_list]
    
    # Get the number and types of reactions on the issue
    reactions_list = card.find_all('div', {'class': 'reaction-summary-item'})
    reaction_counts = {}
    for reaction in reactions_list:
        reaction_type = reaction.find('g-emoji')['alias']
        reaction_count = reaction.find('span', {'class': 'reaction-summary-item-count'}).text.strip()
        reaction_counts[reaction_type] = reaction_count
    
    # Add the data to our lists
    open_closed.append(status)
    comments.append(comment_count)
    contributors.append(contributor_names)
    reactions.append(reaction_counts)

# Create a DataFrame to hold the scraped data
df = pd.DataFrame({'Status': open_closed, 'Comments': comments, 'Contributors': contributors, 'Reactions': reactions})

# Convert the reaction counts to columns
df = pd.concat([df.drop(['Reactions'], axis=1), df['Reactions'].apply(pd.Series)], axis=1)

# Save the DataFrame to a CSV file
df.to_csv('trc-data.csv', index=False)

# Print some statistics about the scraped data
print(f'Total number of issues: {len(df)}')
print(f'Number of open issues: {len(df[df["Status"]=="Open"])}')
print(f'Number of closed issues: {len(df[df["Status"]=="Closed"])}')
print(f'Total number of comments: {df["Comments"].str.replace(",", "").astype(int).sum()}')
