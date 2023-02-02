# @Time    : 22/08/15 15:13
# @Author  : fyq
# @File    : supplier_pay.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.interface_pay import InterfacePay
import pay.constant as pc
from pay.attribute.attribute import Attribute
from pay.file_parser.payable.supplier.supplier_file_parser import SupplierFileParser


class SupplierPay(InterfacePay):

    def order(self) -> int:
        return 1

    def pay_options(self):
        return ("pay", "应付汇总"), ("prepay", "预付汇总")

    def pay_name(self):
        return "supplier", "供应商"

    def __init__(self):
        super().__init__()
        self._attribute_manager_dict["other"].insert(name=pc.write_sheet,
                                                     attribute=Attribute(name=pc.write_detail_sheet,
                                                                         value="",
                                                                         text="[解析]写入的详情工作簿名称",
                                                                         required=True,
                                                                         data_type="str"))
        self._file_parser = SupplierFileParser()
