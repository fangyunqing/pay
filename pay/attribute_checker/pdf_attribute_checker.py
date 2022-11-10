# @Time    : 22/11/10 10:07
# @Author  : fyq
# @File    : pdf_attribute_checker.py
# @Software: PyCharm

__author__ = 'fyq'


from pay.attribute_checker.attribute_checker import IAttributeChecker
from pay.attribute_checker.common_checker import CommonChecker
import pay.constant as pc


class PDFAttributeChecker(IAttributeChecker):

    def create_check_map(self):
        def _check_pdf_file(attribute):
            """
                检测 pdf_file
            :param attribute:
            :return:
            """
            CommonChecker.check_pdf_file(attribute.text, attribute.value)

        def _check_use_column(attribute):
            """
                检测有用的列
            :param attribute:
            :return:
            """
            column_list = []
            for column in attribute.value.split(","):
                column_list.append(CommonChecker.check_excel_map(attribute.text, column))
            attribute.value = ",".join(column_list)

        def _check_write_sheet(attribute):
            """
                写入的工作簿
            :return:
            """
            attribute.value = CommonChecker.check_write_sheet(attribute.text, attribute.value)

        return {
            pc.pdf_file: _check_pdf_file,
            pc.use_column: _check_use_column,
            pc.write_sheet: _check_write_sheet
        }
