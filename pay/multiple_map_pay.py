# @Time    : 22/11/09 16:55
# @Author  : fyq
# @File    : multiple_map_pay.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.attribute.attribute import Attribute
from pay.file_parser.multiple_map import AntiDumpingFileParser
from pay.interface_pay import InterfacePay
from pay.path_parser import DeepPathParser
import pay.constant as pc


class MultipleMapPay(InterfacePay):

    def pay_name(self):
        return "multiple_map", "多文件对照"

    def pay_options(self):
        return ("multiple_map", "多文件对照"),

    def __init__(self):
        super(MultipleMapPay, self).__init__()
        am = self._attribute_manager_dict["other"]
        self._file_parser = [AntiDumpingFileParser()]
        self._path_parser = DeepPathParser()
        am.clear()
        am.add(attribute=Attribute(name=pc.write_sheet,
                                   value="",
                                   text="[模板]写入的工作簿名称[工作簿名,行]",
                                   data_type="str",
                                   required=True))
        am.add(attribute=Attribute(name=pc.category,
                                   value="",
                                   text="所属类型",
                                   data_type="combobox",
                                   required=True,
                                   cb_values=["反倾销"]))

    def pay_type(self, attribute_name, am):
        return am.value(pc.category)
