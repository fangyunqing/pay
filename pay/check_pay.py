# @Time    : 22/11/09 10:19
# @Author  : fyq
# @File    : check_py.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.attribute.attribute import Attribute
from pay.attribute_checker import CheckAttributeChecker
from pay.file_parser.check import DefaultCheckFileParser
from pay.interface_pay import InterfacePay
import pay.constant as pc
from pay.path_parser.simple_path_parser import SimplePathParser


class CheckPay(InterfacePay):

    def pay_name(self):
        return "check", "校对"

    def pay_options(self):
        return ("check", "校对"),

    def __init__(self):
        super(CheckPay, self).__init__()
        self._path_parser = SimplePathParser()
        am = self._attribute_manager_dict["other"]
        self._attribute_checker_list = [CheckAttributeChecker()]
        self._file_parser = DefaultCheckFileParser()
        am.clear()
        am.add(attribute=Attribute(name=pc.data_file,
                                   value="",
                                   text="[数据文件]信息[文件名,工作簿名,跳过的行数]",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.use_column,
                                   value="",
                                   text="[数据文件]需要的列(A,B,C)",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.check_data,
                                   value="",
                                   text="[数据文件]校对列(A:B,C:D)",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.group_column,
                                   value="",
                                   text="[数据文件]分组的列(A,B,C)",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.sort_column,
                                   value="",
                                   text="[数据文件]排序列(A)",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.write_sheet,
                                   value="",
                                   text="[模板]写入的工作簿名称[工作簿名,行]",
                                   data_type="str",
                                   required=True))
        am.add(attribute=Attribute(name=pc.check_result,
                                   value="",
                                   text="[模板]校对结果 result1,result2 eg 剔除,拆单 ",
                                   data_type="str",
                                   required=True))


