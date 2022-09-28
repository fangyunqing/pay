# @Time    : 22/09/27 10:03
# @Author  : fyq
# @File    : default_create_describe_4_excel.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.create_describe_4_excel.create_describe_4_excel import CreateDescribe4Excel
import pay.constant as pc
from pay.describe_excel import DescribeExcel


class DefaultCreateDescribe4Excel(CreateDescribe4Excel):

    def write_sheet_list(self, attribute_manager):
        return [attribute_manager.value(pc.write_sheet)]

    def create_describe_4_excel(self, df_list, attribute_manager):
        write_sheet_list = self.write_sheet_list(attribute_manager)
        describe_excel_list = []
        for index, df in enumerate(df_list):
            if df is None:
                continue
            # 合计行
            total_row_list = []
            for row_index, row in df.iterrows():
                for cell in row:
                    if cell == "合计":
                        total_row_list.append(row_index)
                        break
            # 第一列
            first_row_index = []
            vc = df.iloc[0].value_counts()
            for v in df.iloc[0].unique():
                first_row_index.append(vc[v])

            if len(write_sheet_list) - 1 >= index:
                write_sheet = write_sheet_list[index]
            else:
                write_sheet = write_sheet_list[len(write_sheet_list) - 1]
            write_sheet_info = list(write_sheet.split(","))
            describe_excel = DescribeExcel()
            describe_excel.df = df
            describe_excel.row = len(df.index)
            describe_excel.column = len(df.columns)
            describe_excel.sheet_name = write_sheet_info[0]
            describe_excel.start_row = int(write_sheet_info[1])
            describe_excel.start_column = int(write_sheet_info[2])
            describe_excel.total_row = total_row_list
            describe_excel.first_row_index = first_row_index
            describe_excel.detail = True if index > 0 else False
            describe_excel_list.append(describe_excel)

        return describe_excel_list
