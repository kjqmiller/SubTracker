import csv
import math
import datetime
import boto3
import botocore.exceptions
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

"""
Plots data, saves it to a file locally and/or opens it in a local window. Can choose between "today", "yesterday", or "custom_date" for data to plot.
Choose on line 29 inside str() function
"""
# Choose a date that you'd like to plot the data for. Files stored in s3 are named with 'YYYY-MM-DD.csv' format
today = datetime.datetime.utcnow().date()
yesterday = today - datetime.timedelta(days=1)
custom_date = '2021-11-01'  # Format is 'YYYY-MM-DD'
title_date = None

# Create arrays with values for x and y axes for each data sets
online_y = []
subscribers_y = []
time_object_x = []
percent_online = []

# Connect to s3 and then open the desired CSV on line 25 and append the data to the above arrays for plotting
s3_client = boto3.client('s3')
bucket = 'your_bucket'
csv_to_plot_path = 'data_folder/' + str(custom_date) + '.csv'
downloaded_csv_name = 'data.csv'
try:
    today_csv = s3_client.download_file(bucket, csv_to_plot_path, downloaded_csv_name)
    with open('data.csv') as file:
        reader = csv.reader(file)
        next(reader)
        first = True
        for row in reader:
            if first:
                title_date = row[3]
                first = False
            subscribers_y.append(int(row[0]))
            online_y.append(int(row[1]))
            timestamp = row[2]
            time_object = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
            time_object_x.append(time_object)
            percent_online.append(float(row[5]))

        # Set size of window for figure, set x-axis datetime format, and convert datetime object into numpy array
        plt.figure(figsize=(14, 7.5))
        xformatter = mdates.DateFormatter('%H:%M')
        x = np.array(time_object_x)

        # Plot arrays for total/active sub counts
        fig1 = plt.subplot(2, 2, 1)
        fig1.xaxis.set_major_formatter(xformatter)
        plt.plot(x, online_y, label='Online Subs', color='#318223')
        plt.plot(x, subscribers_y, label='Total Subs', color='#d47a31')
        plt.xticks(rotation=90)
        plt.xlabel('UTC Time')
        plt.ylabel('Total Subs vs Online Subs')
        plt.title('Total vs Online Subs for ' + str(title_date))
        plt.grid(axis='y')
        plt.legend()

        # Plot total subs
        fig2 = plt.subplot(2, 2, 2)
        fig2.xaxis.set_major_formatter(xformatter)
        plt.plot(x, subscribers_y, label='Total Subs', color='#d47a31')
        plt.xticks(rotation=90)
        plt.xlabel('UTC Time')
        plt.ylabel('Total Subs')
        plt.title('Total Subs for ' + str(title_date))
        plt.grid(axis='y')
        plt.grid(axis='x')
        plt.legend()

        # Plot online subs
        fig3 = plt.subplot(2, 2, 3)
        fig3.xaxis.set_major_formatter(xformatter)
        plt.plot(x, online_y, label='Online Subs', color='#318223')
        plt.xticks(rotation=90)
        plt.xlabel('UTC Time')
        plt.ylabel('Online Subs')
        plt.title('Online Subs for ' + str(title_date))
        plt.grid(axis='y')
        plt.legend()

        # Plot percentage online
        percent_high = math.ceil(max(percent_online))
        percent_low = math.floor(min(percent_online))
        labels = [str(i) for i in percent_online]
        fig4 = plt.subplot(2, 2, 4)
        fig4.xaxis.set_major_formatter(xformatter)
        plt.plot(x, percent_online, label='Percent Online')
        plt.ylim([percent_low, percent_high])
        plt.xticks(rotation=90)
        plt.xlabel('UTC Time')
        plt.ylabel('Percent Online')
        plt.title('Percentage of Subscribers Currently Online for ' + str(title_date))
        plt.grid(axis='y', color='k')
        plt.legend()

        # Adjust subplot spacing to make axis labels easier to read
        plt.subplots_adjust(left=0.2, bottom=0.2, right=None, top=None, wspace=None, hspace=1)

        plt.tight_layout()
        plt.savefig('/path/to/file/' + str(title_date) + '.jpg')
        # plt.show()

except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("CSV does not exist, try another date. Make sure the date is in the format 'YYYY-MM-DD'")
