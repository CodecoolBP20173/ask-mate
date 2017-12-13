import time

def display_time(act_time):
    act_time = time.localtime(act_time)
    year = str(act_time.tm_year)
    month = str(act_time.tm_mon)
    month = '0' + month if len(month) < 2 else month
    day = str(act_time.tm_mday)
    day = '0' + day if len(day) < 2 else day
    hour = str(act_time.tm_hour)
    hour = '0' + hour if len(hour) < 2 else hour
    minute = str(act_time.tm_min)
    minute = '0' + minute if len(minute) < 2 else minute
    date = ".".join([year, month, day])
    hour_minute = ":".join([hour, minute])
    result = " ".join([date, hour_minute])
    return result

