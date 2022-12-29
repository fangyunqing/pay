# @Time    : 22/12/29 15:05
# @Author  : fyq
# @File    : attr_util.py
# @Software: PyCharm

__author__ = 'fyq'

from copy import deepcopy


def copy_attr(src, desc):
    src_dict = src.__dict__
    desc_dict = desc.__dict__
    for desc_attr in desc_dict.keys():
        if desc_attr in src_dict.keys():
            setattr(desc, desc_attr, deepcopy(getattr(src, desc_attr)))
