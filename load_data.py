import csv
import boto3
import pandas as pd
import botocore.exceptions
from datetime import datetime


"""
Get dictionary from previous function and convert to DataFrame. Then convert DF into CSV and stage it in s3. Next, either append to current
day's CSV file, or create a new one for the first read of the day. Finally, upload final product to s3.
"""
def load_data(data_dict):
    # Connect to s3
    s3_client = boto3.client('s3')
    print('Connected to s3')

    # Stage data as CSV in s3
    # In order to upload directly to s3, s3fs must be installed. s3fs builds upon botocore and fsspec.
    df = pd.DataFrame([data_dict])
    df.to_csv('s3://your_bucket/staging_data_folder/staging_file.csv', index=False)
    print('Staged CSV')

    # Arguments to download from s3 staging to Lambda /tmp/ folder
    bucket = 'your_bucket'
    staged_s3_path = 'staging_data_folder/staging_file.csv'
    lambda_staged_csv_path = '/tmp/staging_file.csv'

    # Download staged CSV to /tmp/ directory in Lambda
    s3_client.download_file(bucket, staged_s3_path, lambda_staged_csv_path)
    print('Retrieved staged CSV')

    # Arguments to try and append to current day CSV or create new CSV for the day
    today_date = str(datetime.utcnow().date())
    today_s3_path = ('data_folder/' + today_date + '.csv')
    today_lambda_csv_name = ('/tmp/' + today_date + '.csv')
    s3_data_path = ('data_folder/' + today_date + '.csv')

    # Try to download CSV with current date from s3 and append staging.csv, if it fails create new CSV for today
    try:
        s3_client.download_file(bucket, today_s3_path, today_lambda_csv_name)
        with open(lambda_staged_csv_path, 'r') as staged:  # Open staged.csv, skip the header, then read the remaining
            reader = csv.reader(staged)
            next(reader)
            staged_csv = staged.read()
        with open(today_lambda_csv_name, 'a') as today:  # Open today.csv and append the read portion of staged.csv
            today.write(staged_csv)
        s3_client.upload_file(today_lambda_csv_name, bucket, s3_data_path)  # Upload today.csv to s3
    # If there is no existing today.csv  except block will create a new CSV for today using staged.csv
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("Today's CSV does not exist. Creating a new one.")
            s3_client.upload_file(lambda_staged_csv_path, bucket, s3_data_path)  # Upload staged.csv as today.csv
        else:
            raise
