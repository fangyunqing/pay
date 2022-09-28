# @Time    : 22/09/27 9:40
# @Author  : fyq
# @File    : create_describe_4_excel.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import ABCMeta, abstractmethod


class CreateDescribe4Excel(metaclass=ABCMeta):

    @abstractmethod
    def create_describe_4_excel(self, df_list, attribute_manager):
        pass

    @abstractmethod
    def write_sheet_list(self, attribute_manager):
        pass
