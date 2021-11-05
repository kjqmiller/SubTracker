# SubTracker - online/total subreddit user tracker
## Introduction
This application was built to track, over time, the number of total and online subscribers for a chosen subreddit. AWS EventBridge triggers are sent to AWS Lambda, which then runs scripts to pull data from the Reddit API using PRAW. The data is then staged in AWS S3, transformed in Lambda, and finally loaded back into another S3 bucket for storage.
![Project Diagram](https://drive.google.com/uc?export=view&id=1OiLP-s0g3Jnr5zVPIIyGrcGtgeYuGaLK/)

## Table of Contents
* [Why?](#why?)
* [Technologies](#technologies) 
* [Overview](#overview)
  * reddit.py
  * call_reddit_api.py
  * clean_and_organize_data.py
  * load_data.py
  * plot_data.py
* [Setup](#setup)
* [Startup](#startup)
* [Key Lessons Learned](#key-lessons-learned) 

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
* AWS Cloudwatch
* AWS EventBridge
* Praw 7.4.0
* Pandas 1.2.4
* Numpy 1.21.2
* Boto3 1.18.44
* Matplotlib 3.4.3
* Botocore 1.20.106

## Overview
### reddit.py
`reddit.py` is the main file that completes the whole data pipeline by calling the functions defined in the included `.py` files. At the top of the file the  helper functions are imported from the other files, and they are called from within the `Handler()` function. `Handler()` is the function that AWS Lambda calls when it runs the deployment package containing our files and dependencies. `Handler()` accepts two arguments, `event` and `context`. These are Lambda specific but not relevant for this project, so they are both set equal to `None`. Before any of the helper functions are called we must choose which subreddit we would like to collect data for by setting `subreddit = 'chosen_subreddit'`, examples have been provided using subreddits that exist as of the current date (Nov-01-2021).

### call_reddit_api.py
Here we extract the data we want from Reddit.
This file contains the function `get_data()` which is passed the subreddit assigned to `subreddit` in `Handler()` as its argument.

A Reddit instance is assigned to `reddit` using `praw.Reddit()` which accepts your Reddit application's client secret and id, as well as `user_agent` which is in the format `OS:reddit_application_name:vX.X (by /u/<your_reddit_username>)`. 

We then create an object for our chosen subreddit with `sub_data = reddit.subreddit()` and extract the data we need, followed by the creation of a timestamp. Once we have the data we want assigned to variables, we create an empty dictionary to contain all of our data in a single object. Using a for-loop we iterate through the keys we want the dictionary to have, and use the `locals()` function to assign the values from our local variables to the keys in our new dictionary.

Finally, we return the newly created dictionary so that the next function in `reddit.py` can use it.

In the event anything goes wrong, such as a failed API connection, the `try` block will fail and a notification will be printed via the `except` block to AWS CloudWatch logs, including the timestamp.

### clean_and_organize_data.py
Here we update the dictionary returned by `call_reddit_api.py` with additional key:value pairs. This file contains the function `update_dictionary()` which is passed the dictionary returned from `get_data()`.

`data_dict` is updated using the `.update()` method to create three new keys (`date`, `time`, and `percent_online`). `date` and `time` are assigned values by using the `datetime` library to extract only the necessary data from the `timestamp` key. We calculate `percent_online` and multiply by 100 to have an easy to read percentage, then round it to two decimal places using `round()`.

Lastly we return the updated `data_dict`. We print a success or failure messaged based on if the `try` block is successful or not.

### load_data.py
The function `load_data()` in this file performs the most complex part of the application. Firstly it converts `data_dict` into a Pandas DataFrame, it then stages `data_dict` as a CSV file in an S3 bucket. The CSV is then retrieved from the staging area and downloaded into the Lambda `/tmp/` directory. Filenames and paths are assigned to variables as strings in order to make the following code easier to read. 

A `try` block will attempt to download an existing CSV with today's date from S3, if successful it will append the staged data to today's data. If there is not yet a CSV for today, an exception will be raised, prompting the staged CSV to be uploaded as `todays_date.csv`.

### plot_data.py
Allows the choice to plot data from yesterday, today, or a custom date using `matplotlib`. Empty arrays are created to hold the data for each axis. Once created, we connect to S3 and set up variables for arguments. The CSV for the chosen date is downloaded, opened, and each row (except header) is appended to the empty arrays for plotting. Finally, we plot the data and open the charts in a new window for viewing.

## Setup
#### **Disclaimer - A major lesson learned with the project was to better document the learning process. As I am making this README after finishing, I may have forgotten or otherwise made mistakes on some setup details. Hopefully though the following should work, or at least get you on the right path.** 

### Setting up Reddit account and developer application
* You will need to create a Reddit instance using PRAW. In order to do this you must have a Reddit account which, if you don't already have one, can be created [here](https://www.reddit.com/register/?dest=https%3A%2F%2Fwww.reddit.com%2F). After you have an account, follow the **First Steps** found [here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) to set up your application and get your `client_id` and `client_secret`.

### Setting up AWS account
* You will need to set up an Amazon Web Services (AWS) account in order to use the services this application runs on (EventBridge, Lambda, CloudWatch, and Simple Storage Service (S3), which can be done [here](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/). 

### Setting up Lambda
* Lambda runtime was set as Python 3.7 despite the app being written in 3.9 due to versioning issues while isntalling dependencies. 
* When setting up runtime the *Handler* area is where you select which method for Lambda to invoke. It will be in the format `main_filename.method_name`. For example, if you have a file named `main.py` and a method called `do_something()`, you will enter `main.do_something` as your Handler.
* Under *Lambda > Runtime Settings > Architecture* select x86_64.
* A role will be needed for your Lambda function with several permissions to access the various services. To do this go to *Lambda > Functions > your_function > Configuration > Permissions > edit Execution Role*. From there you can create a new role with no template and a timeout set to 5 minutes, this is so you don't get a false timeout if the connection to the API is slow but working. Once you have a role you can add the permissions `AmazonS3FullAccess`, `AWSLambdaBasicExecutionRole`, and `CloudWatchLambdaInsightsExecutionRolePolicy`. These roles will allow read/write access to S3, allow Lambda function executions on your behalf, and grant access to Lambda Insights.
* Logs and `print()` statements will be sent to AWS CloudWatch.

### Setting up EventBridge
* Create trigger from Lambda by chosing *Create Rule*, then give it a name and an optional description.
* Choose whether or not you want the trigger to be sent on a schedule based on interval (set intervals but no specific start times) or with a CRON expression (can specify both size of interval as well as start time). CRON expressions must be in the format `cron(* * * * ? *)` and include at least one `?`.
* Once you decide on a schedule you will set up a Target by choosing *Lambda function* and then lastly selecting `your_function` from the dropdown.
* 
### Setting up Cloudwatch
* If I recall, the Lambda function should automatically send logs to a log group.

### Setting up S3
* Before starting setup, one important thing to know is that S3 is a flat file system that uses objects and keys stored within buckets. Meaning all files are held in a single directory, as opposed to a hierarchical file system like what you'd find on a PC or Mac. As a result, the "folders" that you see in S3 are purly for human readability and the files in them are objects whose keys are the "path" to find them. You can read more about this [here](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html). Understanding this system and its naming conventions will save you a lot of time and headaches.
* Under S3 you will create a new bucket, choose a name and leave the settings as the default.
* Inside your bucket create three (3) folders named `data`, `staging_data`, and `zip_file`. These will store your daily data, your staged data, and your deployment package.

### Deploying Code
* **IMPORTANT - When downloading your dependencies, make sure that you are downloading for the correct OS. AWS runs on Linux so you should download Linux compatable dependencies. For example, if you are running locally on MacOS you cannot use your local MacOS dependencies.**
* Now you will create your deployment package, this is a `.zip` file containing your application and all dependencies.
* Ensure in Lambda you are using x86_64 architecture in your runtime.
* You can find a list of dependencies with `pip3 install pipreqs` and running `pipreqs` in the directory of your Python scripts. This will generate a `requirements.txt` file in that folder.
* Create a folder for your deployment package on your local machine to store your Python files and dependencies in.
* All of your dependencies will have to be downloaded manually and have filenames ending in `x86_64.whl` or `none-any.whl`. They also need to be Python 3.7. These dependencies can be found by seaching [PyPi](https://pypi.org/) and navigating to *Download files*.
* From the command line `cd` into your directory and uncompress each `.zip` file with the command `unzip filename.whl`. Once all files are uncompressed, in the command line use `zip -r your_deployment_package_name.zip .` to zip up all of your files and dependencies.
* Upload your deployment package to the `zip_file` directory of your S3 bucket and when complete, navigate to your file and copy its URL.
* Go back to your function navigate to *Code > Code source > Upload from > S3 location* and paste in the URL for your deployment package.

### Startup
* Now that everything should be set up navigate back to EventBridge, select your rule, and click *Enable*.
* The pipeline will run until the rule is disabled.
* Check that things are running smoothly by going back to Lambda and clicking *Monitor > View logs in CloudWatch*. The logs are where any error messages will be sent to. In the event you get an error, assuming it due to bad code or missing dependencies, you must fix the error locally and upload an updated deployment package to S3 following the same steps from above. 

### Key Lessons Learned
* Probably the most important lesson I learned throughout this project is to throughly document your successes and failures. Lots of hours were lost searching for a fix to something I broke, only becuase I could not remember how I got it to work in the first place. The same goes for ensuring I don't repeat application breaking mistakes once I've made them. Good documentation also helps reinforce learning and makes creating documentation for others much easier and more thorough.
* The biggest challenge by far was figuring out how to deploy the project with AWS. The list goes on, but notable lessons were making sure dependencies are compatable with AWS, understanding the S3 file system, and creating a deployment package that would run.

