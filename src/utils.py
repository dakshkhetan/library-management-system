from datetime import datetime, timedelta

todays_date = datetime.today()


def change_day():
    global todays_date
    todays_date = todays_date + timedelta(days=1)
    print(f"Date changed to: {todays_date.date()}")


def reset_todays_date():
    global todays_date
    todays_date = datetime.today()
    return todays_date


def get_todays_date():
    global todays_date
    print(f"Returning date: {todays_date.date()}")
    return todays_date


def get_date_diff(datetime1, datetime2):
    return datetime1.date() - datetime2.date()
