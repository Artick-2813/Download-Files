import datetime


def time():
    current_time = datetime.datetime.today().strftime("%H:%M")
    return current_time


def date():
    current_date = datetime.date.today()
    return current_date


def date_time():
    current_date = date()
    current_time = time()
    current_date_time = str(current_date) + ' ' + str(current_time)
    return current_date_time

