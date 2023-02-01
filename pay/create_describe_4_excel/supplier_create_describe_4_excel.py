# @Time    : 23/02/01 10:30
# @Author  : fyq
# @File    : supplier_create_describe_4_excel.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.create_describe_4_excel import TotalCreateDescribe4Excel
import pay.constant as pc


class SupplierCreateDescribe4Excel(TotalCreateDescribe4Excel):

    def write_sheet_list(self, attribute_manager):
        write_sheet_list = super().write_sheet_list(attribute_manager)
        write_sheet_list.append(attribute_manager.value(pc.write_detail_sheet))
        return write_sheet_list
