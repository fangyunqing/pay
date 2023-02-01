# @Time    : 23/02/01 10:11
# @Author  : fyq
# @File    : total_create_describe_4_excel.py
# @Software: PyCharm

__author__ = 'fyq'

from pandas import DataFrame

from pay.attribute import AttributeManager
from pay.create_describe_4_excel import DefaultCreateDescribe4Excel
from pay.create_describe_4_excel.describe_excel import DescribeExcel, TotalDescribeExcel
import pandas as pd


class TotalCreateDescribe4Excel(DefaultCreateDescribe4Excel):

    def _do_create_describe_4_excel(self, de: DescribeExcel, df: DataFrame, write_sheet: str, index: int,
                                    attribute_manager: AttributeManager) -> None:
        super()._do_create_describe_4_excel(de, df, write_sheet, index, attribute_manager)
        if isinstance(de, TotalDescribeExcel):
            # 合计行
            total_row_list = []
            for row_index, row in df.iterrows():
                for cell in row:
                    if cell == "合计":
                        total_row_list.append(row_index)
                        break
            # 第一列合并单元格的节点数
            first_column_merger_list = []
            vc = df["0"].value_counts()
            for v in df["0"].unique():
                if not pd.isna(v):
                    first_column_merger_list.append(vc[v])

            de.total_row_list = total_row_list
            de.first_column_merger_list = first_column_merger_list

    def new_describe_excel(self) -> DescribeExcel:
        return TotalDescribeExcel()
