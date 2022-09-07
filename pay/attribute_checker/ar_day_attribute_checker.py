# @Time    : 22/08/29 16:10
# @Author  : fyq
# @File    : ar_day_attribute_checker.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.attribute_checker.attribute_checker import IAttributeChecker
from pay.attribute_checker.common_checker import CommonChecker
import pay.constant as pc


class ARDayAttributeChecker(IAttributeChecker):

    def create_check_map(self):

        def _check_client_map(attribute):
            """
                检测对照文件
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_sheet_info(attribute.text, attribute.value)

        def _check_ar_day_data(attribute):
            """
                检测数据文件
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_sheet_info(attribute.text, attribute.value)

        def _check_pay_date(attribute):
            """
                日期列
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_ar_money(attribute):
            """
                应付金额列
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_currency(attribute):
            """
                币种列
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_water_bill_code(attribute):
            """
                水单客户编码
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_ar_begin_date(attribute):
            """
                单据开始时间
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_date(attribute.text, attribute.value)

        def _check_ar_end_date(attribute):
            """
                单据结束时间
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_date(attribute.text, attribute.value)

        def _check_map_water_bill_code(attribute):
            """
                对照表水单客户编码
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_map_bill_code(attribute):
            """
                对照表客户编码列
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_bill_code(attribute):
            """
                模板客户编码列
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_begin_date(attribute):
            """
                日期起始列
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_pay_recv(attribute):
            pay_recv_list = list(attribute.value.split(","))
            if len(pay_recv_list) < 3:
                raise Exception("配置项[%s]:[%s]格式必须为 应收,已收,未收" % (attribute.text, attribute.value))
            column_list = []
            for column in pay_recv_list:
                column_list.append(CommonChecker.check_excel_map(attribute.text, column))
            attribute.value = ",".join(column_list)

        def _check_write_sheet(attribute):
            """
                写入的工作簿
            :return:
            """
            attribute.value = CommonChecker.check_write_sheet(attribute.text, attribute.value)

        def _check_pay_currency(attribute):
            """
                模板币种列
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_map_client_name(attribute):
            """
                对照客户名称列
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_pay_client_name(attribute):
            """
                模板客户对照列
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        def _check_water_client_name(attribute):
            """
                出纳水单客户对照列
            :param attribute:
            :return:
            """
            attribute.value = CommonChecker.check_excel_map(attribute.text, attribute.value)

        return {
            pc.ar_day_data: _check_ar_day_data,
            pc.client_map: _check_client_map,
            pc.water_bill_code: _check_water_bill_code,
            pc.pay_date: _check_pay_date,
            pc.ar_money: _check_ar_money,
            pc.currency: _check_currency,
            pc.ar_begin_date: _check_ar_begin_date,
            pc.ar_end_date: _check_ar_end_date,
            pc.map_water_bill_code: _check_map_water_bill_code,
            pc.map_bill_code: _check_map_bill_code,
            pc.bill_code: _check_bill_code,
            pc.begin_date: _check_begin_date,
            pc.pay_recv: _check_pay_recv,
            pc.write_sheet: _check_write_sheet,
            pc.pay_currency: _check_pay_currency,
            pc.map_client_name: _check_map_client_name,
            pc.pay_client_name: _check_pay_client_name,
            pc.water_client_name: _check_water_client_name
        }
