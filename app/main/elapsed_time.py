from datetime import datetime

old = datetime.now()


def elapsed_time(old):
    new = datetime.now()
    print((old - new))
    return old - new


def to_string(time):
    time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f').date()
    print(time, type(time))
    return time


elapsed_time(old)
