# @Time    : 22/12/17 16:15
# @Author  : fyq
# @File    : diff_type.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import ABCMeta, abstractmethod


class DiffType(metaclass=ABCMeta):

    @abstractmethod
    def support(self):
        pass

    @abstractmethod
    def handle(self, map_df, data_df,
               map_diff, data_diff, diff_column_name,
               point_equal,
               single_express, express_param_one, express_param_two,
               stat,
               total_s):
        pass
