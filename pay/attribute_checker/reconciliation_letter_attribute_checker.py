# @Time    : 23/02/25 10:12
# @Author  : fyq
# @File    : reconciliation_letter_attribute_checker.py
# @Software: PyCharm

__author__ = 'fyq'

from typing import Dict, Callable

from pay.attribute import Attribute
from pay.attribute_checker.attribute_checker import IAttributeChecker
from pay.attribute_checker.common_checker import CommonChecker
from pay.constant import attr_string


class ReconciliationLetterAttributeChecker(IAttributeChecker):

    def create_check_map(self) -> Dict[str, Callable[[Attribute], None]]:
        def _check_location(attribute: Attribute):
            """
                   位置信息
               :param attribute:
               :return:
               """
            attribute.value = CommonChecker.check_location_item(attribute.text, attribute.value)

        def _check_map(attribute):
            """
                数据文件
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_sheet_info(attribute.text, attribute.value)

        def _check_excel_map(attribute):
            """
                排序列
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        return {
            attr_string.location_company: _check_location,
            attr_string.location_opening_currency: _check_location,
            attr_string.location_pay_currency: _check_location,
            attr_string.location_back_currency: _check_location,
            attr_string.location_person: _check_location,
            attr_string.data_file: _check_map,
            attr_string.check_column: _check_excel_map,
        }
