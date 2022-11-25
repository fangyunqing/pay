# @Time    : 22/11/18 13:57
# @Author  : fyq
# @File    : str_util.py
# @Software: PyCharm

__author__ = 'fyq'


def remove_zero(val):
    val = str(val)
    val_list = list(val.split("."))
    if len(val_list) > 1:
        for v in val_list[1:]:
            if len(v) * '0' != v:
                return val.strip('0')
        return val_list[0]
    else:
        return val
