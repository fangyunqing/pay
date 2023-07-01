# @Time    : 2023/07/01 9:58
# @Author  : fyq
# @File    : freeze_pay.py
# @Software: PyCharm

__author__ = 'fyq'

from typing import Tuple

from pay.attribute import common_attribute
from pay.file_parser.freeze import FreezeFileParser
from pay.interface_pay import InterfacePay
from pay.path_parser import DeepPathParser


class FreezePay(InterfacePay):

    def __init__(self):
        super(FreezePay, self).__init__()
        am = self._attribute_manager_dict["other"]
        am.clear()
        am.add(common_attribute.info_attr)
        self._file_parser = FreezeFileParser()
        self._path_parser = DeepPathParser()

    def pay_name(self) -> Tuple[str, str, bool]:
        return "freeze", "冻结", False

    def pay_options(self) -> Tuple[Tuple[str, str], ...]:
        return ("freeze", "冻结"),

    def order(self) -> int:
        return 20
