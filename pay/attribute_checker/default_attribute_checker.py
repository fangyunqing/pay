# @Time    : 22/08/11 11:18
# @Author  : fyq
# @File    : default_attribute_checker.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.attribute_checker.common_checker import CommonChecker
import pay.constant as pc
from pay.attribute_checker.attribute_checker import IAttributeChecker


class DefaultAttributeChecker(IAttributeChecker):
    """
        默认的属性检查器
    """

    def create_check_map(self):
        def _check_read_sheet(attribute):
            """
                读取的工作簿
            :return:
            """
            pass

        def _check_skip_rows(attribute):
            """
                跳过的行数
            :return:
            """
            attribute.value = CommonChecker.check_digit_ge(attribute.text, attribute.value)

        def _check_use_column(attribute):
            """
                需要的列
            :return:
            """
            column_list = []
            for column in attribute.value.split(","):
                column_list.append(CommonChecker.check_excel_map(attribute.text, column))
            attribute.value = ",".join(column_list)

        def _check_sort_column(attribute):
            """
                排序列
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_supplier_column(attribute):
            """
                供应商列
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_type_column(attribute):
            """
                供应商类型列号
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_write_sheet(attribute):
            """
                写入的工作簿
            :return:
            """
            attribute.value = CommonChecker.check_write_sheet(attribute.text, attribute.value)

        def _check_write_detail_sheet(attribute):
            """
                写入的详情工作簿
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_write_sheet(attribute.text, attribute.value)

        def _check_check(attribute):
            """
                校对
            :return:
            """
            attribute.value = CommonChecker.check_subtraction(attribute.text, attribute.value)

        def _check_no_pay_reason(attribute):
            """
                未请款原因
            :param attribute:
            :return:
            """
            column_list = []
            for column in attribute.value.split(","):
                column_list.append(CommonChecker.check_excel_map(attribute.text, column))
            attribute.value = ",".join(column_list)

        def _check_pur_group(attribute):
            """
                采购组织
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_pur_no(attribute):
            """
                请购单号
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_pre_pay(attribute):
            """
                预付余额分析
            :param attribute:
            :return:
            """
            column_list = []
            for column in attribute.value.split(","):
                column_list.append(CommonChecker.check_excel_map(attribute.text, column))
            attribute.value = ",".join(column_list)

        return {
            pc.check: _check_check,
            pc.sort_column: _check_sort_column,
            pc.supplier_column: _check_supplier_column,
            pc.type_column: _check_type_column,
            pc.skip_rows: _check_skip_rows,
            pc.use_column: _check_use_column,
            pc.read_sheet: _check_read_sheet,
            pc.write_sheet: _check_write_sheet,
            pc.write_detail_sheet: _check_write_detail_sheet,
            pc.no_pay_reason: _check_no_pay_reason,
            pc.pur_group: _check_pur_group,
            pc.pur_no: _check_pur_no,
            pc.pre_pay: _check_pre_pay
        }

