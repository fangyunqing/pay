# @Time    : 22/09/27 10:03
# @Author  : fyq
# @File    : default_create_describe_4_excel.py
# @Software: PyCharm

__author__ = 'fyq'

import typing

from pandas import DataFrame

from pay.attribute import AttributeManager
from pay.create_describe_4_excel.abstract_create_describe_4_excel import AbstractCreateDescribe4Excel
import pay.constant as pc
from pay.create_describe_4_excel.describe_excel import DescribeExcel
import pandas as pd


class DefaultCreateDescribe4Excel(AbstractCreateDescribe4Excel):

    def _do_create_describe_4_excel(self, de: DescribeExcel, df: DataFrame, write_sheet: str, index: int,
                                    attribute_manager: AttributeManager) -> None:
        write_sheet_info = list(write_sheet.split(","))
        de.df = df
        de.row_count = len(df.index)
        de.column_count = len(df.columns)
        de.sheet_name = write_sheet_info[0]
        de.start_row = int(write_sheet_info[1])
        de.start_column = int(write_sheet_info[2])
        de.detail = True if index > 0 else False

    def new_describe_excel(self) -> DescribeExcel:
        return DescribeExcel()

    def write_sheet_list(self, attribute_manager):
        return [attribute_manager.value(pc.write_sheet)]
