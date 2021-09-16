import matplotlib.pyplot as plt
import csv
import datetime

# Get the date for today and previous day
# TODO add loop to run through all previous files when plotting
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)

# Create arrays with values for x and y axes for each data sets
online_y = []
subscribers_y = []
time_x = []
percent_online = []

# Open the desired CSV and append the data to the previous arrays for plotting, making sure not
# to append the header rows as well.
with open('/Users/samanthawillis/reddit_user_project/data/' + str(today) + '.csv') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        subscribers_y.append(int(row[0]))
        online_y.append(int(row[1]))
        # Remove trailing digits from seconds to make graph more readable
        time = row[4]
        time = time[:-10]
        time_x.append(time)
        percent_online.append(float(row[5]))

    # Set size of window for plot
    plt.figure(figsize=(10, 7.5))

    #   Plot arrays for total/active sub counts
    plt.subplot(2, 1, 1)
    plt.plot(time_x, online_y, label='Online Subs', color='#318223')
    plt.plot(time_x, subscribers_y, label='Total Subs', color='#d47a31')
    plt.xticks(rotation=90)
    plt.xlabel('UTC Time')
    plt.ylabel('Total Subs vs Online Subs')
    plt.title('Total vs Online Subs for ' + str(today))
    plt.grid(axis='y')
    plt.legend()

    # Plot percentage online
    labels = [str(i) for i in percent_online]
    plt.subplot(2, 1, 2)
    plt.plot(time_x, percent_online)
    plt.ylim([0, 10])
    plt.xticks(rotation=90)
    plt.xlabel('UTC Time')
    plt.ylabel('Percent Online')
    plt.title('Percentage of Subscribers Currently Online for ' + str(today))
    plt.grid(axis='y', color='k')

    # Adjust subplot spacing to make axis labels easier to read
    plt.subplots_adjust(left=0.2, bottom=0.2, right=None, top=None, wspace=None, hspace=1)

    plt.show()
