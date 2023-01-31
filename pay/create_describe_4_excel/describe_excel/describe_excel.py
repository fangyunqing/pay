# @Time    : 22/08/12 16:23
# @Author  : fyq
# @File    : describe_excel.py
# @Software: PyCharm

__author__ = 'fyq'

from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class DescribeExcel:

    """
        描述excel信息 用于写入excel 和 渲染excel
        df DataFrame对象
        row 行数
        column 列数
        sheet_name 工作簿名称
        start_row 起始行
        start_column 结束行
    """
    df: DataFrame

    row: int

    column: int

    sheet_name: str

    start_row: int

    start_column: int

