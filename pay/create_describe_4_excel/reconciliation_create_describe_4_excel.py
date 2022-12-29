# @Time    : 22/09/27 16:48
# @Author  : fyq
# @File    : reconciliation_create_describe_4_excel.py
# @Software: PyCharm

__author__ = 'fyq'


from pay.create_describe_4_excel.default_create_describe_4_excel import DefaultCreateDescribe4Excel
import pay.constant as pc
from pay.create_describe_4_excel.describe_excel import MapDescribeExcel


class ReconciliationCreateDescribe4Excel(DefaultCreateDescribe4Excel):

    def new_describe_excel(self):
        return MapDescribeExcel()

    def _do_other(self, index, describe_excel, df, write_sheet_info):
        pass

    def write_sheet_list(self, attribute_manager):
        write_sheet_list = super(ReconciliationCreateDescribe4Excel, self).write_sheet_list(attribute_manager)
        write_sheet_list.append(attribute_manager.value(pc.write_not_found_sheet))
        write_sheet_list.append(attribute_manager.value(pc.write_total_sheet))
        return write_sheet_list

