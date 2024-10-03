import datetime

from digatron_utility.read import time_to_seconds


def test_time_to_seconds():
    string = "01:02:03"
    assert time_to_seconds(string) == 3723
    dt0 = datetime.datetime(2021, 5, 20, 11, 41, 28)
    dt1 = datetime.datetime(2021, 5, 20, 12, 43, 31)
    assert time_to_seconds(dt1 - dt0) == 3723
