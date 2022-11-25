# @Time    : 22/11/11 14:57
# @Author  : fyq
# @File    : check_attribute_checker.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.attribute_checker.attribute_checker import IAttributeChecker
from pay.attribute_checker.common_checker import CommonChecker
import pay.constant as pc


class CheckAttributeChecker(IAttributeChecker):

    def create_check_map(self):

        def _check_data_file(attribute):
            """
                数据文件
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_sheet_info(attribute.text, attribute.value)

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

        def _check_check_data(attribute):
            """
                校对数据
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_check_data(attribute.text, attribute.value)

        def _check_group_column(attribute):
            """
                聚合列
            :param attribute:
            :return:
            """
            column_list = []
            for column in attribute.value.split(","):
                column_list.append(CommonChecker.check_excel_map(attribute.text, column))
            attribute.value = ",".join(column_list)

        def _check_check_result(attribute):
            """
                校对结果
            :param attribute:
            :return:
            """
            CommonChecker.check_check_result(attribute.text, attribute.value)

        def _check_sort_column(attribute):
            """
                排序列
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        return {
            pc.data_file: _check_data_file,
            pc.write_sheet: _check_write_sheet,
            pc.use_column: _check_use_column,
            pc.check_data: _check_check_data,
            pc.group_column: _check_group_column,
            pc.check_result: _check_check_result,
            pc.sort_column: _check_sort_column
        }
