import praw
from datetime import datetime


def get_data(subreddit):
    try:
        # Create a read-only Reddit instance with praw
        reddit = praw.Reddit(
            client_id='your_client_id',
            client_secret='your_secret_id',
            user_agent='your_OS:reddit_application_name:vX.X (by /u/<your_reddit_username>)'
        )

        # Get all data available for the chosen subreddit, then select relevant data and add timestamp
        sub_data = reddit.subreddit(subreddit)
        subscribers = sub_data.subscribers
        online = sub_data.accounts_active
        timestamp = datetime.utcnow()

        # Convert variables into a dictionary for easy use with pandas
        data_dict = {}
        for i in ('subscribers', 'online', 'timestamp'):
            data_dict[i] = locals()[i]

        print('Data retrieved successfully at ' + str(data_dict['timestamp']) + ' UTC')
        return data_dict

    except Exception:
        print('Data retrieval failed at ' + str(datetime.utcnow()) + ' UTC')
