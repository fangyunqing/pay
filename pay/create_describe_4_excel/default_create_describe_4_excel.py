# @Time    : 22/09/27 10:03
# @Author  : fyq
# @File    : default_create_describe_4_excel.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.create_describe_4_excel.abstract_create_describe_4_excel import AbstractCreateDescribe4Excel
import pay.constant as pc
from pay.create_describe_4_excel.describe_excel import DescribeExcel


class DefaultCreateDescribe4Excel(AbstractCreateDescribe4Excel):

    def new_describe_excel(self):
        return DescribeExcel()

    def _do_other(self, index, describe_excel, df, write_sheet_info):
        pass

    def write_sheet_list(self, attribute_manager):
        return [attribute_manager.value(pc.write_sheet)]
