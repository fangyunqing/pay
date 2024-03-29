# @Time    : 22/09/27 9:40
# @Author  : fyq
# @File    : create_describe_4_excel.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import ABCMeta, abstractmethod
import typing

from pandas import DataFrame

from pay.attribute import AttributeManager
from pay.create_describe_4_excel.describe_excel import DescribeExcel


class CreateDescribe4Excel(metaclass=ABCMeta):

    @abstractmethod
    def create_describe_4_excel(self, df_list: typing.List[DataFrame],
                                attribute_manager: AttributeManager) -> typing.List[DescribeExcel]:
        pass


