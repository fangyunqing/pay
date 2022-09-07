# @Time    : 22/08/26 15:47
# @Author  : fyq
# @File    : ar_day_pay.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.attribute_checker.ar_day_attribute_checker import ARDayAttributeChecker
from pay.file_copy.no_file_copy import NoFileCopy
from pay.file_parser.ar_day_file_parser import ARDayFileParser
from pay.interface_pay import InterfacePay
from pay.attribute.attribute import Attribute
import pay.constant as pc
from pay.path_parser.simple_path_parser import SimplePathParser


class ARDayPay(InterfacePay):

    def pay_name(self):
        return "ap_day", "应收每日"

    def pay_options(self):
        return ("ap_day", "应收每日"),

    def __init__(self):
        super(ARDayPay, self).__init__()
        self._attribute_checker_list = [ARDayAttributeChecker()]
        am = self._attribute_manager_dict["other"]
        self._file_copy = NoFileCopy()
        self._file_parser = ARDayFileParser()
        self._path_parser = SimplePathParser()
        am.clear()
        am.add(attribute=Attribute(name=pc.ar_day_data,
                                   value="",
                                   text="出纳收款单文件信息[文件名,工作簿名,跳过的行数]",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.client_map,
                                   value="",
                                   text="客户对照文件信息[文件名,工作簿名,跳过的行数]",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.water_bill_code,
                                   value="",
                                   text="[出纳收款单]水单客户代码列",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.water_client_name,
                                   value="",
                                   text="[出纳收款单]水单客户名称列",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.pay_date,
                                   value="",
                                   text="[出纳收款单]日期列",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.ar_money,
                                   value="",
                                   text="[出纳收款单]收款金额列",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.currency,
                                   value="",
                                   text="[出纳收款单]币种列",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.ar_begin_date,
                                   value="",
                                   text="[出纳收款单]开始时间",
                                   required=True,
                                   data_type="date"))
        am.add(attribute=Attribute(name=pc.ar_end_date,
                                   value="",
                                   text="[出纳收款单]结束时间",
                                   required=True,
                                   data_type="date"))
        am.add(attribute=Attribute(name=pc.map_water_bill_code,
                                   value="",
                                   text="[客户对照]水单客户代码列",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.map_bill_code,
                                   value="",
                                   text="[客户对照]客户代码列",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.map_client_name,
                                   value="",
                                   text="[客户对照]客户名称列",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name="write_sheet",
                                   value="",
                                   text="[模板]写入的工作簿名称",
                                   data_type="str",
                                   required=True))
        am.add(attribute=Attribute(name=pc.bill_code,
                                   value="",
                                   text="[模板]客户代码列",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.pay_client_name,
                                   value="",
                                   text="[模板]客户名称列",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.pay_currency,
                                   value="",
                                   text="[模板]币种列",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.begin_date,
                                   value="",
                                   text="[模板]日期起始列",
                                   required=True,
                                   data_type="str"))
        am.add(attribute=Attribute(name=pc.pay_recv,
                                   value="",
                                   text="[模板]应收,已收,未收列",
                                   required=True,
                                   data_type="str"))