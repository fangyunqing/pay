# @Time    : 22/09/27 10:38
# @Author  : fyq
# @File    : write_excel.py
# @Software: PyCharm

__author__ = 'fyq'


from abc import ABCMeta, abstractmethod


class WriteExcel(metaclass=ABCMeta):

    @abstractmethod
    def write_excel(self, describe_excel_list, attribute_manager, target_file):
        pass
