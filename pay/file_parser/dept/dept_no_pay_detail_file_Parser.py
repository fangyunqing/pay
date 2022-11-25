# @Time    : 22/08/17 10:13
# @Author  : fyq
# @File    : dept_no_pay_detail_file_Parser.py
# @Software: PyCharm

__author__ = 'fyq'

import pay.constant as pc
import pandas as pd

from pay.file_parser.dept.abstract_other_column_file_parser import AbstractOtherColumnFileParser


class DeptNoPayDetailFileParser(AbstractOtherColumnFileParser):

    def support(self, pay_type):
        return pay_type == "dept.no_pay_detail"

    def _other_column(self, attribute_manager):
        no_pay_reason_column = [int(c) for c in attribute_manager.value(pc.no_pay_reason).split(",")]
        no_pay_reason_column.sort()
        return no_pay_reason_column

    def _group_column(self, attribute_manager):
        return [attribute_manager.value(pc.supplier_column),
                attribute_manager.value(pc.type_column),
                attribute_manager.value(pc.pur_group),
                *attribute_manager.value(pc.no_pay_reason).split(",")]

    def __init__(self):
        super().__init__()
        self._insert_name = False

    def _ignore(self):
        return True
