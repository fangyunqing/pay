# @Time    : 22/08/16 11:47
# @Author  : fyq
# @File    : dept_pay.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.attribute.attribute import Attribute
from pay.file_parser.payable.dept import DeptNoVerificationFileParser
from pay.interface_pay import InterfacePay
from pay.path_parser.dept_path_parser import DeptPathParser
import pay.constant as pc
import copy
from pay.file_parser.payable.dept import DeptFileParser
from pay.file_parser.payable.dept import DeptPayDetailFileParser
from pay.file_parser.payable.dept import DeptNoPayDetailFileParser
from pay.file_parser.payable.dept import DeptPrePayDetailFileParser


class DeptPay(InterfacePay):

    def order(self) -> int:
        return 3

    def pay_name(self):
        return "dept", "事业部"

    def pay_options(self):
        return ("pay", "应付汇总"), ("prepay", "预付汇总"), \
               ("pay_detail", "应付-采购明细表"), ("pre_pay_detail", "预付-采购明细表"), \
               ("no_pay_detail", "应付-未请款明细说明"), ("no_verification", "预付-未核销说明")

    def __init__(self):
        super().__init__()
        self._path_parser = DeptPathParser()
        am = self._attribute_manager_dict["other"]
        pay_detail_am = copy.deepcopy(am)
        pay_detail_am.insert(name=pc.supplier_column,
                             attribute=Attribute(name=pc.pur_group,
                                                 value="",
                                                 text="[解析]采购组织列(单列)",
                                                 required=True,
                                                 data_type="str"))
        pay_detail_am.insert(name=pc.pur_group,
                             attribute=Attribute(name=pc.pur_no,
                                                 value="",
                                                 text="[解析]请购单号列(单列)",
                                                 required=True,
                                                 data_type="str"))
        self._attribute_manager_dict["pay_detail"] = pay_detail_am

        pre_pay_detail_am = copy.deepcopy(am)
        pre_pay_detail_am.insert(name=pc.supplier_column,
                                 attribute=Attribute(name=pc.pur_group,
                                                     value="",
                                                     text="[解析]采购组织列(单列)",
                                                     required=True,
                                                     data_type="str"))
        pre_pay_detail_am.insert(name=pc.pur_group,
                                 attribute=Attribute(name=pc.pur_no,
                                                     value="",
                                                     text="[解析]请购单号列(单列)",
                                                     required=True,
                                                     data_type="str"))
        pre_pay_detail_am.insert(name=pc.use_column,
                                 attribute=Attribute(name=pc.pre_pay,
                                                     value="",
                                                     text="[解析]已预付余额分析(多列,逗号分隔)",
                                                     required=True,
                                                     data_type="str"))
        self._attribute_manager_dict["pre_pay_detail"] = pre_pay_detail_am

        no_pay_detail_am = copy.deepcopy(am)
        no_pay_detail_am.insert(name=pc.supplier_column,
                                attribute=Attribute(name=pc.pur_group,
                                                    value="",
                                                    text="[解析]采购组织列(单列)",
                                                    required=True,
                                                    data_type="str"))
        no_pay_detail_am.insert(name=pc.use_column,
                                attribute=Attribute(name=pc.no_pay_reason,
                                                    value="",
                                                    text="[解析]未请款原因列(多列,逗号分隔)",
                                                    required=False,
                                                    data_type="str"))
        self._attribute_manager_dict["no_pay_detail"] = no_pay_detail_am

        no_pay_detail_am = copy.deepcopy(am)
        no_pay_detail_am.insert(name=pc.supplier_column,
                                attribute=Attribute(name=pc.pur_group,
                                                    value="",
                                                    text="[解析]采购组织列(单列)",
                                                    required=True,
                                                    data_type="str"))
        no_pay_detail_am.insert(name=pc.use_column,
                                attribute=Attribute(name=pc.no_verification,
                                                    value="",
                                                    text="[解析]未核销原因(多列,逗号分隔)",
                                                    required=False,
                                                    data_type="str"))
        self._attribute_manager_dict["no_verification"] = no_pay_detail_am

        self._file_parser = [DeptFileParser(),
                             DeptNoPayDetailFileParser(),
                             DeptPrePayDetailFileParser(),
                             DeptPayDetailFileParser(),
                             DeptNoVerificationFileParser()]
