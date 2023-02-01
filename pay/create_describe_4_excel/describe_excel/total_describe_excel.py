# @Time    : 22/12/20 14:34
# @Author  : fyq
# @File    : total_describe_excel.py
# @Software: PyCharm

__author__ = 'fyq'

from dataclasses import dataclass, field

from pay.create_describe_4_excel.describe_excel import DescribeExcel
import typing


@dataclass
class TotalDescribeExcel(DescribeExcel):
    """
       total_row_list 合计行
       first_column_merger_list 第一行合并节点

    """
    total_row_list: typing.List[int] = field(default=None)

    first_column_merger_list: typing.List[int] = field(default=None)
