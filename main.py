from call_reddit_api import get_data
from clean_and_organize_data import update_dictionary
from load_data import load_data


def Handler(event=None, context=None):
    # Select a subreddit without the "/r" (examples: 'learnpython', 'pics', 'Python', 'stocks', 'LifeProTips')
    subreddit = 'subreddit_to_track'

    # Get dictionary of data from chosen subreddit
    data = get_data(subreddit)

    # Update dictionary with any transformations or additional calculations
    updated_data = update_dictionary(data)

    # Stage data in s3 bucket, then append staged data to current CSV, or create new CSV if none exists
    load_data(updated_data)
