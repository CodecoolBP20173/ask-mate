import time

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def display_time(act_time):

    """
    :param act_time as a float: the UNIX timestamp
    :returns date as a string: 'yyyy.mm.dd hh:mm'
    """
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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def display_unix_time():

    """
    :returns UNIX timestamp of current time as a float
    """
    return time.time()

def order_list_by_submission_time(list_of_dict):
    """
    Re-orders a list of dictionaries in descending order based on the value of the "submission_time"
    key.
    param: list of dictionaries
    return: list of dictionaries ordered by submission_time
    """
    for iterations in range(len(list_of_dict)):
        current = 0
        while current <= len(list_of_dict) - 2:
            if float(list_of_dict[current + 1]["submission_time"]) > float(list_of_dict[current]["submission_time"]):
                list_of_dict[current], list_of_dict[current+1] = list_of_dict[current+1], list_of_dict[current]
            current += 1
        iterations += 1
    return list_of_dict