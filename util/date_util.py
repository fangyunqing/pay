# @Time    : 22/11/09 13:22
# @Author  : fyq
# @File    : date_util.py
# @Software: PyCharm

__author__ = 'fyq'

import time


def format_date(date_str):
    try:
        if "/" in date_str:
            return time.strptime(date_str, "%Y/%m/%d")
        else:
            return time.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None
