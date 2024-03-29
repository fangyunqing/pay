# @Time    : 22/08/15 15:08
# @Author  : fyq
# @File    : group_pay.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.interface_pay import InterfacePay
import pay.constant as pc
from pay.attribute.attribute import Attribute
from pay.file_parser.payable.group.group_file_parser import GroupFileParser


class GroupPay(InterfacePay):

    def order(self) -> int:
        return 2

    def pay_options(self):
        return ("pay", "应付汇总"), ("prepay", "预付汇总"), ("no-pay", "应付未付款")

    def pay_name(self):
        return "group", "集团"

    def __init__(self):
        super(GroupPay, self).__init__()
        self._attribute_manager_dict["other"].insert(name=pc.sort_column,
                                                     attribute=Attribute(name=pc.dept,
                                                                         value="",
                                                                         text="[模板]部门",
                                                                         required=True,
                                                                         data_type="str"))
        self._file_parser = GroupFileParser()
