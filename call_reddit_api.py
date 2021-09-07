import praw
# from pprint import pprint
from datetime import datetime


def get_data(main_subreddit):
    try:
        # Create a read-only Reddit instance with praw
        # In order to create an authorized instance you will also need your username and password
        reddit = praw.Reddit(
            client_id='ESay_-NgRDJ5Vp_V2OWgTA',
            client_secret='7u7tOsjMt2h9t1nC_5n4aVQ5fL7y-g',
            user_agent='MacOS:collect_user_counts:v1.0 (by /u/<Pastextian>)'
        )

        # Get all data available for the chosen subreddit
        sub_data = reddit.subreddit(main_subreddit)
        subscribers = sub_data.subscribers
        online = sub_data.accounts_active
        timestamp = datetime.utcnow()
        print(str(online) + ' online')
        print(str(subscribers) + ' subscribers')

        # Convert variables into a dictionary for easy use with pandas
        data = {}
        for i in ('subscribers', 'online', 'timestamp'):
            data[i] = locals()[i]

        print('Data retrieved successfully at ' + str(data['timestamp']) + ' UTC')
        return data

    except Exception:
        print('Data retrieval failed at ' + str(datetime.utcnow()) + ' UTC')

# for key in sub_dict:
#     print(key + ': ' + str(sub_dict[key]))

# Print all available attributes for an object, in this case it is the subreddit object
# Trying to print the name of the subreddit causes a network request to be made because praw objects are lazy
# and won't make a request unless additional information is needed
# print(sub_data.name)
# pprint(vars(sub_data))
