# @Time    : 22/12/20 8:36
# @Author  : fyq
# @File    : singleton.py
# @Software: PyCharm

__author__ = 'fyq'


def singleton(cls):
    _instance_dict = {}

    def inner(*args, **kwargs):
        if cls not in _instance_dict:
            _instance_dict[cls] = cls(*args, **kwargs)
        return _instance_dict.get(cls)

    return inner
