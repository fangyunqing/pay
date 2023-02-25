# @Time    : 23/02/09 8:42
# @Author  : fyq
# @File    : handle_column.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import ABCMeta, abstractmethod

import typing

from pandas import DataFrame

from pay.attribute import AttributeManager


class HandleColumn(metaclass=ABCMeta):

    @abstractmethod
    def handle_column(self, df_list: typing.List[DataFrame], attribute_manager: AttributeManager):
        pass
