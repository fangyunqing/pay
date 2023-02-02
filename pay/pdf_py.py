# @Time    : 22/11/09 10:19
# @Author  : fyq
# @File    : pdf_py.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.attribute.attribute import Attribute
from pay.attribute_checker import PDFAttributeChecker
from pay.file_parser.pdf.wei_lin_pdf_file_parser import WeiLinPafFileParser
from pay.interface_pay import InterfacePay
from pay.path_parser.pdf_path_parser import PdfPathParser
import pay.constant as pc


class PdfPay(InterfacePay):

    def order(self) -> int:
        return 6

    def pay_name(self):
        return "PDF", "PDF"

    def pay_options(self):
        return ("PDF", "PDF"),

    def __init__(self):
        super(PdfPay, self).__init__()
        self._path_parser = PdfPathParser()
        am = self._attribute_manager_dict["other"]
        self._file_parser = [WeiLinPafFileParser()]
        self._attribute_checker_list = [PDFAttributeChecker()]
        am.clear()
        am.add(attribute=Attribute(name=pc.pdf_file,
                                   value="",
                                   text="[pdf文件]信息[pdf文件名,列数]",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.use_column,
                                   value="",
                                   text="[pdf文件]需要的列(A,B,C)",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.bill_code_prefix,
                                   value="",
                                   text="[pdf文件]单号前缀",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.skip_text,
                                   value="",
                                   text="[pdf文件]每页跳过的文本",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.across_column,
                                   value="",
                                   text="[pdf文件]跨行的列(A)",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.unit,
                                   value="",
                                   text="[pdf文件]单位",
                                   required=False,
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

