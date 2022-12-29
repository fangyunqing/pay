# @Time    : 22/12/29 14:25
# @Author  : fyq
# @File    : abstract_create_describe_4_excel.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import abstractmethod

from pay.create_describe_4_excel.create_describe_4_excel import CreateDescribe4Excel
from pay.create_describe_4_excel.describe_excel import DescribeExcel


class AbstractCreateDescribe4Excel(CreateDescribe4Excel):

    def create_describe_4_excel(self, df_list, attribute_manager):
        write_sheet_list = self.write_sheet_list(attribute_manager)
        describe_excel_list = []
        for index, df in enumerate(df_list):

            write_sheet = self._get_write_sheet(index, write_sheet_list)
            write_sheet_info = list(write_sheet.split(","))
            describe_excel = DescribeExcel()
            describe_excel.df = df
            describe_excel.row = len(df.index)
            describe_excel.column = len(df.columns)
            describe_excel.sheet_name = write_sheet_info[0]
            describe_excel.start_row = int(write_sheet_info[1])
            describe_excel.start_column = int(write_sheet_info[2])

            describe_excel_list.append(describe_excel)

    @abstractmethod
    def write_sheet_list(self, attribute_manager):
        pass

    @staticmethod
    def _get_write_sheet(index, write_sheet_list):
        if len(write_sheet_list) - 1 >= index:
            return write_sheet_list[index]
        else:
            return write_sheet_list[len(write_sheet_list) - 1]
