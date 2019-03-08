import time


def load_function(t):
    """The desired load function from the administra tor.

    Arguments:
        t: The time to sample as a Unix time

    Returns:
        float: The target percent load
    """
    t_local = time.localtime(t)
    if t_local.tm_wday in range(5, 6):
        # If Saturday or Sunday, return 90%
        return .9
    elif t_local.tm_hour in range(8, 17):
        # It is a workday during business hours, return 20%
        return .2
    else:
        # It is a workday out of business hours, return 80%
        return .8
