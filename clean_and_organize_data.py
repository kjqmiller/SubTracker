from datetime import datetime

# Get current user and datetime information from Superstonk and format / add columns
def update_dictionary(main_dict):
    try:
        main_dict.update(
            date=datetime.date(main_dict['timestamp']),
            time=datetime.time(main_dict['timestamp']),
            percent_online=round(((main_dict['online'] / main_dict['subscribers']) * 100), 2)
        )
        print('Dictionary update successful')
        return main_dict
    except Exception:
        print('Dictionary update failed')
