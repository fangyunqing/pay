# @Time    : 22/08/12 16:23
# @Author  : fyq
# @File    : describe_excel.py
# @Software: PyCharm

__author__ = 'fyq'

from dataclasses import dataclass, field

from pandas import DataFrame


@dataclass
class DescribeExcel:

    """
        描述excel信息 用于写入excel 和 渲染excel
        df DataFrame对象
        row_count 行数
        column_count 列数
        sheet_name 工作簿名称
        start_row 起始行
        start_column 结束行
        detail 是否详情
    """
    df: DataFrame = field(default=None)

    row_count: int = field(default=None)

    column_count: int = field(default=None)

    sheet_name: str = field(default=None)

    start_row: int = field(default=None)

    start_column: int = field(default=None)

    detail: bool = field(default=None)

