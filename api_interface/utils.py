import datetime
from external import ApiSpbStuRuz
import datetime


def get_second_monday(year, month):

    res = datetime.datetime(year, month, 1)
    while res.weekday() != 0:
        res += datetime.timedelta(days=1)
    res += datetime.timedelta(days=7)
    return res.day
