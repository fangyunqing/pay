# @Time    : 22/09/27 10:51
# @Author  : fyq
# @File    : reconciliation_pay.py
# @Software: PyCharm

__author__ = 'fyq'


from pay.attribute_checker.reconciliation_attribute_checker import ReconciliationAttributeChecker
from pay.file_parser.map import GreenSampleMaterialFeeFileParser, TeBuProductFileParser, TeBuSampleFileParser, \
    GreenSampleDyeFeeFileParser, GreenSampleFeeFileParser
from pay.file_parser.map.reconciliation_file_parser import ReconciliationFileParser
from pay.interface_pay import InterfacePay
from pay.attribute.attribute import Attribute
import pay.constant as pc
from pay.path_parser.simple_path_parser import SimplePathParser


class ReconciliationPay(InterfacePay):

    def pay_name(self):
        return "reconciliation", "应收对账"

    def pay_options(self):
        return ("reconciliation", "应收对账"),

    def __init__(self):
        super(ReconciliationPay, self).__init__()
        self._attribute_checker_list = [ReconciliationAttributeChecker()]
        self._file_parser = [ReconciliationFileParser(), GreenSampleMaterialFeeFileParser(), TeBuProductFileParser(),
                             TeBuSampleFileParser(), GreenSampleDyeFeeFileParser(), GreenSampleFeeFileParser()]
        self._path_parser = SimplePathParser()
        am = self._attribute_manager_dict["other"]
        am.clear()
        am.add(attribute=Attribute(name=pc.map_file,
                                   value="",
                                   text="[对照文件]信息[文件名,工作簿名,跳过的行数]",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.map_use_column,
                                   value="",
                                   text="[对照文件]需要的列(A,B,C)",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.map_bill_code,
                                   value="",
                                   text="[对照文件]订单号(A)",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.map_spec_column,
                                   value="",
                                   text="[对照文件]特殊的列(A,B,C)",
                                   required=False,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.data_file,
                                   value="",
                                   text="[数据文件]信息[文件名,工作簿名,跳过的行数]",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.data_use_column,
                                   value="",
                                   text="[数据文件]需要的列(A,B,C)",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.data_bill_code,
                                   value="",
                                   text="[数据文件]订单号(A)",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.data_spec_column,
                                   value="",
                                   text="[数据文件]特殊的列(A,B,C)",
                                   required=False,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.map_data,
                                   value="",
                                   text="对照文件和数据文件之间的列对照(A:A:0,B:B:1)",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.write_sheet,
                                   value="",
                                   text="[模板]写入的工作簿名称[工作簿名,1]",
                                   data_type="str",
                                   required=True))
        am.add(attribute=Attribute(name=pc.write_not_found_sheet,
                                   value="",
                                   text="[模板]未找到的工作簿名称[工作簿名,1]",
                                   data_type="str",
                                   required=True))
        am.add(attribute=Attribute(name=pc.write_total_sheet,
                                   value="",
                                   text="[模板]统计的工作簿名称[工作簿名,1]",
                                   data_type="str",
                                   required=True))
        am.add(attribute=Attribute(name=pc.category,
                                   value="",
                                   text="所属类型",
                                   data_type="combobox",
                                   required=True,
                                   cb_values=["常用", "绿洲样品", "绿洲样品-材料费", "绿洲样品-染费", "特步量产", "特步样品"]))

    def pay_type(self, attribute_name, am):
        return am.value(pc.category)




