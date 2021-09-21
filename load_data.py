import csv
import boto3
import botocore.exceptions
import pandas as pd
from datetime import date
import os.path


# Get dictionary from previous function
def load_data(main_updated_dict):
    # Connect to s3
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')

    # Stage data as CSV in s3
    # In order to upload directly to s3, s3fs must be installed. s3fs builds upon botocore and fsspec.
    df = pd.DataFrame([main_updated_dict])
    df.to_csv('s3://reddit-user-data/staging_data/staging.csv')

    # Function arguments
    bucket = 'reddit-user-data'

    # Get staged CSV - works
    staged_csv_path = 'staging_data/staging.csv'
    # TODO eventually the following should be in a lambda /tmp/ folder
    staged_csv_name = 'staging.csv'
    s3_client.download_file(bucket, staged_csv_path, staged_csv_name)

    # Arguments
    today_date = str(date.today())
    today_csv_path = ('data/' + today_date + '.csv')
    today_csv_name = (today_date + '.csv')
    s3_data_path = ('data/' + today_date + '.csv')
    # Try to download csv with current date from s3 and append staging.csv, if it fails create new one and append
    # TODO get index to increment, currently all 0
    try:
        s3_client.download_file(bucket, today_csv_path, today_csv_name)
        with open(staged_csv_name, 'r') as staged:  # Open staged.csv, skip the header, then read the remaining
            reader = csv.reader(staged)
            next(reader)
            staged_csv = staged.read()
        with open(today_csv_name, 'a') as today:  # Open today.csv and append the read portion of staged.csv to it
            today.write(staged_csv)
        s3_client.upload_file(today_csv_name, bucket, s3_data_path)  # Upload today.csv to s3
    # If there is no existing today.csv, create a new one using staged.csv
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("Today's CSV does not exist. Creating a new one with staged.csv.")
            s3_client.upload_file(staged_csv_name, bucket, s3_data_path)  # Upload staged.csv as today.csv
        else:
            raise
