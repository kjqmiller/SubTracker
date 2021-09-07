#!/usr/local/bin/python3.9
from call_reddit_api import get_data
from clean_and_organize_data import update_dictionary
from load_data import load_data

# Select a subreddit
subreddit = 'Superstonk'
# Get dictionary of data from subreddit
data = get_data(subreddit)
# Update dictionary with any transformations or additional calculations
updated_data = update_dictionary(data)
# Convert dictionary to CSV and append
# Check for duplicate data, if so rerun from beginning
load_data(updated_data)
print('==========================')
