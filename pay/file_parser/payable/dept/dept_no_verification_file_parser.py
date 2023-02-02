# @Time    : 22/11/22 13:36
# @Author  : fyq
# @File    : dept_no_verification_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import pay.constant as pc

from pay.file_parser.payable.dept.abstract_other_column_file_parser import AbstractOtherColumnFileParser


class DeptNoVerificationFileParser(AbstractOtherColumnFileParser):

    def _ignore_not_exist(self) -> bool:
        return True

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

