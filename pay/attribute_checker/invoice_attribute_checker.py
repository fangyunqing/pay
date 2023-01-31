# @Time    : 23/01/31 14:26
# @Author  : fyq
# @File    : invoice_attribute_checker.py
# @Software: PyCharm

__author__ = 'fyq'

from typing import Dict, Callable

from pay.attribute import Attribute
from pay.attribute_checker.attribute_checker import IAttributeChecker
from pay.attribute_checker.common_checker import CommonChecker
from pay.constant import attr_string


class InvoiceAttributeChecker(IAttributeChecker):

    def create_check_map(self) -> Dict[str, Callable[[Attribute], None]]:
        def _check_excel_map(attribute):
            """
                excel 字母转成数字
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_skip_rows(attribute):
            """
                跳过的行数
            :return:
            """
            attribute.value = CommonChecker.check_digit_ge(attribute.text, attribute.value)

        return {
            attr_string.skip_rows: _check_skip_rows,
            attr_string.money_column: _check_excel_map,
            attr_string.qty_column: _check_excel_map,
            attr_string.rate_column: _check_excel_map,
            attr_string.kind_column: _check_excel_map,
            attr_string.client_code_column: _check_excel_map,
            attr_string.use_column: _check_excel_map
        }