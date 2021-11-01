# SubTracker - online/total subreddit user tracker
## Introduction
Application to track the number of subscribers for a chosen subreddit, as well as tracking the number of users currently online. The code is ran 
using AWS Lambda and data is stored in CSV format using AWS S3 buckets.

## Table of Contents
* Why?
* Technologies 
* Overview
  * reddit.py
  * call_reddit_api.py
  * clean_and_organize_data.py
  * load_data.py
  * plot_data.py
* Setup
* Key Lessons Learned 

## Why?
I developed this project becuase I wanted to:
  * Create an ETL pipeline using Python
  * Track and visualize the total/online subscriber numbers of a fast growing subreddit I frequent
  * Learn how to deploy a project on the cloud using AWS technologies
  * Grow my portfolio of projects and learn new skills/technologies

## Technologies
* Python 3.9
* AWS S3
* AWS Lambda
* Praw 7.4.0
* Pandas 1.2.4
* Numpy 1.21.2
* Boto3 1.18.44
* Matplotlib 3.4.3
* Botocore 1.20.106

## Overview
### reddit.py
`reddit.py` is the main file that completes the whole data pipeline by calling the functions defined in the included `.py` files.
At the top of the file the helper functions are imported from the other files, and they are called from within the `Handler()` function.
`Handler()` is the function that AWS Lambda calls when it runs the deployment package containing our files and dependencies.
`Handler()` accepts two arguments, `event` and `context`. These are Lambda specific but not relevant for this project, so they are 
both set equal to `None`. Before any of the helper functions are called we must choose which subreddit we would like to collect data for by 
setting `subreddit = 'chosen_subreddit'`, examples have been provided using subreddits that exist as of the current date (Nov-01-2021).

### call_reddit_api.py
Here we extract the data we want from Reddit.
This file contains the function `get_data()` which is passed the subreddit assigned to `subreddit` in `Handler()` as its argument.

A Reddit instance is assigned to `reddit` using `praw.Reddit()` which accepts your Reddit application's client secret and id, as well as `user_agent` which is in the format `OS:reddit_application_name:vX.X (by /u/<your_reddit_username>)`. 

We then create an object for our chosen subreddit with `sub_data = reddit.subreddit()` and extract the data we need, followed by the creation of a timestamp. Once we have the data we want assigned to variables, we create an empty dictionary to contain all of our data in a single object. Using a for-loop we iterate through the keys we want the dictionary to have, and use the `locals()` function to assign the values from our local variables to the keys in our new dictionary.

Finally, we return the newly created dictionary so that the next function in `reddit.py` can use it.

In the event anything goes wrong, such as a failed API connection, the `try` block will fail and a notification will be printed via the `except` block to AWS CloudWatch logs, including the timestamp.

### clean_and_organize_data.py
Here we update the dictionary returned by `call_reddit_api.py` with additional key:value pairs.
This file contains the function `update_dictionary()` which is passed the dictionary returned from `get_data()`.

`data_dict` is updated using the `.update()` method to create three new keys (`date`, `time`, and `percent_online`). `date` and `time` are assigned values by using the `datetime` library to extract only the necessary data from the `timestamp` key. We calculate `percent_online` and multiply by 100 to have an easy to read percentage, then round it to two decimal places using `round()`.

Lastly we return the updated `data_dict`. We print a success or failure messaged based on if the `try` block is successful or not.

### load_data.py
The function `load_data()` in this file performs the most complex part of the application. Firstly it converts `data_dict` into a Pandas DataFrame, it then stages `data_dict` as a CSV file in an S3 bucket. The CSV is then retrieved from the staging area and downloaded into the Lambda `/tmp/` directory. Filenames and paths are assigned to variables as strings in order to make the following code easier to read. 

A `try` block will attempt to download an existing CSV with today's date from S3, if successful it will append the staged data to today's data. If there is not yet a CSV for today, an exception will be raised, prompting the staged CSV to be uploaded as `todays_date.csv`.

### plot_data.py
Allows the choice to plot data from yesterday, today, or a custom date using `matplotlib`. 
Empty arrays are created to hold the data for each axis. Once created, we connect to S3 and set up variables for arguments.
The CSV for the chosen date is downloaded, opened, and each row (except header) is appended to the empty arrays for plotting. 
Finally, we plot the data and open the charts in a new window for viewing.

## Setup
#### Disclaimer - A major lesson learned with the project was to better document the learning process. As I am making this README after finishing, I may have forgotten or otherwise made mistakes on some setup details. Hopefully though the following should work, or at least get you on the right path. 

### Setting up Reddit account and developer application
You will need to create a Reddit instance using praw. In order to do this you must have a Reddit account which, if you don't already have one, can be created [here](https://www.reddit.com/register/?dest=https%3A%2F%2Fwww.reddit.com%2F). After you have an account, follow the **First Steps** found [here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) to set up your application and get your `client_id` and `client_secret`.

### Setting up AWS account
* Get `.pem` file
* Setting up roles, permissions, IAM, etc

### Setting up Lambda
* Runtime ended up Python 3.7
* Needed to add `/tmp/` to deployment
* Set up to run `reddit.Handler()`
* Printing to log groups

### Setting up EventBridge
* Running with CRON or interval
* Connect to Lambda as a trigger

### Setting up Cloudwatch
* Set up log groups 

### Setting up S3
* Flat file system

### Deploying Code
* Creating deployment package
* Terminal command to remove excess files
* Making sure to download `linux_any` versions of dependencies with correct Python versions
* Zipping files/folders and uploading to S3
* Connecting Lambda to S3 deployment package location





