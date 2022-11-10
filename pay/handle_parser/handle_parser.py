# @Time    : 22/09/27 13:50
# @Author  : fyq
# @File    : handle_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import ABCMeta, abstractmethod


class HandleParser(metaclass=ABCMeta):

    @abstractmethod
    def handle_parser(self, file_dict, file_info, use_column_list):
        pass
