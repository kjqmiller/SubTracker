from datetime import datetime


"""
Takes existing dictionary and adds new columns by extracting only the date and time from timestamp, also adds a percent_online column.
"""
# Use timestamp from data_dict to add date, time, and percent_online
def update_dictionary(data_dict):
    try:
        data_dict.update(
            date=datetime.date(data_dict['timestamp']),
            time=datetime.time(data_dict['timestamp']),
            percent_online=round(((data_dict['online'] / data_dict['subscribers']) * 100), 2)
        )
        print('Dictionary update successful')
        return data_dict
    except Exception:
        print('Dictionary update failed')
