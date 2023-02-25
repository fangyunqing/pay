# @Time    : 23/02/09 9:58
# @Author  : fyq
# @File    : invoice_2_pay.py
# @Software: PyCharm

__author__ = 'fyq'

from typing import Tuple

from pay.attribute import common_attribute
from pay.attribute_checker import InvoiceAttributeChecker
from pay.file_parser.invoice2 import Invoice2FileParser
from pay.interface_pay import InterfacePay
from pay.path_parser.simple_path_parser import SimplePathParser


class Invoice2Pay(InterfacePay):

    def pay_name(self) -> Tuple[str, str]:
        return "invoice2", "开票申请书(合并)"

    def pay_options(self) -> Tuple[Tuple[str, str], ...]:
        return ("invoice2", "开票申请书(合并)"),

    def order(self) -> int:
        return 10

    def __init__(self):

        def _key(key: str):
            if "-" in key:
                return key.split("-")[-1]
            else:
                return key

        super(Invoice2Pay, self).__init__()
        # 属性设置
        am = self._attribute_manager_dict["other"]
        am.clear()
        am.add(common_attribute.read_sheet_attr)
        am.add(common_attribute.skip_rows_attr)
        am.add(common_attribute.use_columns_attr)
        am.add(common_attribute.skip_text_attr)
        am.add(common_attribute.write_sheet_attr)
        # 文件解析器
        self._file_parser = Invoice2FileParser()
        # 属性检查
        self._attribute_checker_list = [InvoiceAttributeChecker()]
        # 路径解析
        self._path_parser = SimplePathParser(_key)
