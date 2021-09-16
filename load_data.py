import csv
import pandas as pd
import os.path


# Get dictionary from previous function
def load_data(main_updated_dict):
    # Stage data as CSV
    df = pd.DataFrame([main_updated_dict])
    staging_csv_path = '/Users/samanthawillis/reddit_user_project/staging_data/staging.csv'
    df.to_csv(staging_csv_path)

#   If CSV with current date exists, append the row
    current_date_path = '/Users/samanthawillis/reddit_user_project/data/' + str(df['date'][0]) + '.csv'
    if os.path.exists(current_date_path):
        df.to_csv(current_date_path, mode='a', index=False, header=False)
        print('Data appended')
    # If CSV with current date does NOT exist, create it and append the staged csv
    else:
        with open(current_date_path, 'w'):
            print('New file created')
            df.to_csv(current_date_path, mode='a', index=False)
            print('First row added to new file')