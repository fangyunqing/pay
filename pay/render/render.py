# @Time    : 22/09/28 8:52
# @Author  : fyq
# @File    : render.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import ABCMeta, abstractmethod
import typing


from pay.attribute import AttributeManager
from pay.create_describe_4_excel.describe_excel import DescribeExcel


class Render(metaclass=ABCMeta):

    @abstractmethod
    def render(self,
               describe_excel_list: typing.List[DescribeExcel],
               attribute_manager: AttributeManager,
               target_file: str) -> None:
        pass

