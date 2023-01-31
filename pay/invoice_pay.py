# @Time    : 23/01/31 13:27
# @Author  : fyq
# @File    : invoice_pay.py
# @Software: PyCharm

__author__ = 'fyq'

from typing import Tuple

from pay.attribute_checker import InvoiceAttributeChecker
from pay.interface_pay import InterfacePay
from pay.attribute import common_attribute
from pay.path_parser import InvoicePathParser


class InvoicePay(InterfacePay):

    def __init__(self):
        super(InvoicePay, self).__init__()
        # 属性设置
        am = self._attribute_manager_dict["other"]
        am.clear()
        am.add(common_attribute.read_sheet_attr)
        am.add(common_attribute.skip_rows_attr)
        am.add(common_attribute.money_column_attr)
        am.add(common_attribute.qty_column_attr)
        am.add(common_attribute.rate_column_attr)
        am.add(common_attribute.kind_column_attr)
        am.add(common_attribute.use_column_attr)
        am.add(common_attribute.client_code_column_attr)
        # 属性检查
        self._attribute_checker_list = [InvoiceAttributeChecker()]
        # 路径解析
        self._path_parser = InvoicePathParser()

    def order(self) -> int:
        return 9

    def pay_name(self) -> Tuple[str, str]:
        return "invoice", "开票申请书"

    def pay_options(self) -> Tuple[Tuple[str, str], ...]:
        return ("invoice", "开票申请书"),
