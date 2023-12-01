from test_3 import sum_current_time


def test_sum_current_time_0():
    assert sum_current_time("00:00:00") == 0


def test_sum_current_time_1():
    assert sum_current_time("10:04:37") == 51


def test_sum_current_time_2():
    assert sum_current_time("03:02:01") == 6


def test_sum_current_time_3():
    assert sum_current_time("12:04:56") == 72
