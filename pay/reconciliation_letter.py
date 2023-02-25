# @Time    : 23/02/25 9:46
# @Author  : fyq
# @File    : reconciliation_letter.py
# @Software: PyCharm

__author__ = 'fyq'

from copy import copy
from typing import Tuple

from pay.attribute import common_attribute
from pay.attribute_checker import ReconciliationLetterAttributeChecker
from pay.file_parser.reconciliation_letter import ReconciliationLetterFileParser
from pay.interface_pay import InterfacePay
from pay.path_parser import DeepPathParser


class ReconciliationLetter(InterfacePay):

    def pay_name(self) -> Tuple[str, str, bool]:
        # name
        return "reconciliation_letter", "对账函", False

    def pay_options(self) -> Tuple[Tuple[str, str], ...]:
        return ("reconciliation_letter", "对账函"),

    def order(self) -> int:
        return 11

    def __init__(self):
        super().__init__()
        am = self._attribute_manager_dict["other"]
        am.clear()
        map_sheet_attr = copy(common_attribute.data_file_attr)
        map_sheet_attr.text = "对照文件[文件名,工作簿名,跳过的行数]"

        check_column_attr = copy(common_attribute.check_column_attr)
        check_column_attr.text = "检验列(eg: A or 1)"

        am.add(common_attribute.datafile_attr)
        am.add(map_sheet_attr)
        am.add(common_attribute.skip_rows_attr)
        am.add(common_attribute.location_company_attr)
        am.add(common_attribute.location_person_attr)
        am.add(common_attribute.location_opening_currency_attr)
        am.add(common_attribute.location_pay_currency_attr)
        am.add(common_attribute.location_back_currency_attr)
        am.add(common_attribute.check_column_attr)

        # 属性检查
        self._attribute_checker_list = [ReconciliationLetterAttributeChecker()]
        # 路径解析
        self._path_parser = DeepPathParser()
        # 文件解析
        self._file_parser = ReconciliationLetterFileParser()
