# @Time    : 22/09/27 10:03
# @Author  : fyq
# @File    : total_create_describe_4_excel.py
# @Software: PyCharm

__author__ = 'fyq'

import pay.constant as pc
from pay.create_describe_4_excel.default_create_describe_4_excel import DefaultCreateDescribe4Excel
from pay.create_describe_4_excel.describe_excel import TotalDescribeExcel
import pandas as pd


class TotalCreateDescribe4Excel(DefaultCreateDescribe4Excel):

    def new_describe_excel(self):
        return TotalDescribeExcel()

    def _do_other(self, index, describe_excel, df, write_sheet_info):
        total_row_list = []
        for row_index, row in df.iterrows():
            for cell in row:
                if cell == "合计":
                    total_row_list.append(row_index)
                    break
        describe_excel.total_row = total_row_list

        first_row_index = []
        vc = df["0"].value_counts()
        for v in df["0"].unique():
            if not pd.isna(v):
                first_row_index.append(vc[v])
        describe_excel.first_row_index = first_row_index

        # 判断是否是时间类型
        dt_column = []
        for i, v in df.dtypes.items():
            if "time" in v.name:
                dt_column.append(i)
        describe_excel.dt_column = dt_column

        describe_excel.detail = True if index > 0 else False

    def write_sheet_list(self, attribute_manager):
        return [attribute_manager.value(pc.write_sheet)]

