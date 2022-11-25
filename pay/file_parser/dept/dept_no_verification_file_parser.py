# @Time    : 22/11/22 13:36
# @Author  : fyq
# @File    : dept_no_verification_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import pay.constant as pc
import pandas as pd

from pay.file_parser.dept.abstract_other_column_file_parser import AbstractOtherColumnFileParser


class DeptNoVerificationFileParser(AbstractOtherColumnFileParser):

    def _other_column(self, attribute_manager):
        no_verification_column = [int(c) for c in attribute_manager.value(pc.no_verification).split(",")]
        no_verification_column.sort()
        return no_verification_column

    def _group_column(self, attribute_manager):
        return [attribute_manager.value(pc.supplier_column),
                attribute_manager.value(pc.type_column),
                attribute_manager.value(pc.pur_group),
                *attribute_manager.value(pc.no_verification).split(",")]

    def support(self, pay_type):
        return pay_type == "dept.no_verification"

    def __init__(self):
        super().__init__()
        self._insert_name = False

    def _ignore(self):
        return True
