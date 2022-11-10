# @Time    : 22/11/09 10:19
# @Author  : fyq
# @File    : pdf_py.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.attribute.attribute import Attribute
from pay.file_parser.wei_lin_pdf_file_parser import WeiLinPafFileParser
from pay.interface_pay import InterfacePay
from pay.path_parser.pdf_path_parser import PdfPathParser
import pay.constant as pc


class PdfPay(InterfacePay):

    def pay_name(self):
        return "PDF", "PDF"

    def pay_options(self):
        return ("PDF", "PDF"),

    def __init__(self):
        super(PdfPay, self).__init__()
        self._path_parser = PdfPathParser()
        am = self._attribute_manager_dict["other"]
        self._file_parser = [WeiLinPafFileParser()]
        am.clear()
        am.add(attribute=Attribute(name=pc.pdf_file,
                                   value="",
                                   text="[pdf文件]信息[文件名,default,跳过的行数]",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.use_column,
                                   value="",
                                   text="[pdf文件]需要的列(A,B,C)",
                                   required=True,
                                   data_type="str"))
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
                                   cb_values=["威霖"]))

    def pay_type(self, attribute_name, am):
        return am.value(pc.category)
