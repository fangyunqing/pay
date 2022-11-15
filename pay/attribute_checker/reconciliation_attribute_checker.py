# @Time    : 22/09/27 11:29
# @Author  : fyq
# @File    : reconciliation_attribute_checker.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.attribute_checker.attribute_checker import IAttributeChecker
from pay.attribute_checker.common_checker import CommonChecker
import pay.constant as pc


class ReconciliationAttributeChecker(IAttributeChecker):

    def create_check_map(self):
        def _check_map_file(attribute):
            """
                对照文件
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_sheet_info(attribute.text, attribute.value)

        def _check_map_bill_code(attribute):
            """
                对照文件中单号
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_map_use_column(attribute):
            """
                对照文件需要的列
            :return:
            """
            column_list = []
            for column in attribute.value.split(","):
                column_list.append(CommonChecker.check_excel_map(attribute.text, column))
            attribute.value = ",".join(column_list)

        def _check_data_file(attribute):
            """
                数据文件
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_sheet_info(attribute.text, attribute.value)

        def _check_data_bill_code(attribute):
            """
                数据文件中单号
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_data_use_column(attribute):
            """
                数据文件需要的列
            :return:
            """
            column_list = []
            for column in attribute.value.split(","):
                column_list.append(CommonChecker.check_excel_map(attribute.text, column))
            attribute.value = ",".join(column_list)

        def _check_map_data(attribute):
            """
                对照文件和数据文件之间的列对照
            :param attribute:
            :return:
            """
            map_column_list = []
            for map_column in attribute.value.split(","):
                map_column_list.append(CommonChecker.check_map_column(attribute.text, map_column))
            attribute.value = ",".join(map_column_list)

        def _check_write_sheet(attribute):
            """
                写入的工作簿
            :return:
            """
            attribute.value = CommonChecker.check_write_sheet(attribute.text, attribute.value)

        def _check_write_not_found_sheet(attribute):
            """
                未找到的工作簿
            :return:
            """
            attribute.value = CommonChecker.check_write_sheet(attribute.text, attribute.value)

        def _check_spec_column(attribute):
            """
                特殊列
            :param attribute:
            :return:
            """
            if len(attribute.value) > 0:
                column_list = []
                for column in attribute.value.split(","):
                    column_list.append(CommonChecker.check_excel_map(attribute.text, column))
                attribute.value = ",".join(column_list)

        def _check_write_total_sheet(attribute):
            """
                未找到的工作簿
            :return:
            """
            attribute.value = CommonChecker.check_write_sheet(attribute.text, attribute.value)

        return {
            pc.map_file: _check_map_file,
            pc.map_bill_code: _check_map_bill_code,
            pc.map_use_column: _check_map_use_column,
            pc.data_file: _check_data_file,
            pc.data_bill_code: _check_data_bill_code,
            pc.data_use_column: _check_data_use_column,
            pc.map_data:  _check_map_data,
            pc.write_sheet: _check_write_sheet,
            pc.write_not_found_sheet: _check_write_not_found_sheet,
            pc.map_spec_column: _check_spec_column,
            pc.data_spec_column: _check_spec_column,
            pc.write_total_sheet: _check_write_total_sheet
        }
