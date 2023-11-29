from datetime import datetime


def get_time():
    """
    Return a string representing the current time in format "%Y-%m-%d %H:%M:%S.%f"
    :return: str
    """
    return str(datetime.now())


def str_to_time(s):
    """
    Convert a string into a datetime object.
    :param s: str
    :return:
    """
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
