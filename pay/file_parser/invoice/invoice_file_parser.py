# @Time    : 23/01/31 16:51
# @Author  : fyq
# @File    : invoice_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from typing import List, Dict, Iterable

import typing
from pandas import DataFrame
import pandas as pd
import numpy as np

from pay.attribute import AttributeManager
from pay.create_describe_4_excel import DefaultCreateDescribe4Excel
from pay.create_describe_4_excel.describe_excel import DescribeExcel

from pay.file_parser.invoice.abstract_invoice_file_parser import AbstractInvoiceFileParser
from pay.render import DefaultRender
from pay.reset_index.default_reset_index import DefaultResetIndex
from pay.write_excel.default_write_excel import DefaultWriteExcel
from pay.constant import attr_string
from util import pd_read_excel_by_path


class InvoiceFileParser(AbstractInvoiceFileParser):
    """
        需要在excel后增加几列
        add-no 序号
        add-date 开票日期
        add-code 客户编码 + 序号
        add-date-1 开票日期1
        add-money 主营业收入
        add-tax 税额
        add-invoice-money 开票金额
        add-qty 入账数量
        add-kind 类别
    """

    add_no = "add_no"

    add_date = "add_date"

    add_code = "add_code"

    add_date_1 = "add_date_1"

    add_money = "add_money"

    add_tax = "add_tax"

    add_tax_money = "add_tax_money"

    add_qty = "add_qty"

    add_kind = "add_kind"

    def _do_read_file(self, file_dict: Dict[str, Iterable],
                      attribute_manager: AttributeManager) -> Dict[str, List[List[DataFrame]]]:

        def _map(df: DataFrame):
            df.replace(0, np.nan, inplace=True)
            money_column = attribute_manager.value(attr_string.money_column)
            df.dropna(subset=money_column, inplace=True)
            return df

        read_sheet = attribute_manager.value(attr_string.read_sheet)
        skip_rows = attribute_manager.value(attr_string.skip_rows)
        use_columns = attribute_manager.value(attr_string.use_columns)
        df_dict: Dict[str, List[List[DataFrame]]] = {}
        for key in file_dict.keys():
            file_path_list = file_dict[key]
            for file_path in file_path_list:
                df_list = pd_read_excel_by_path(file_path=file_path,
                                                read_sheet=read_sheet,
                                                skip_rows=skip_rows,
                                                use_column=use_columns.split(","),
                                                limit=True,
                                                limit_column=0,
                                                limit_value="合计")

                df_list = list(filter(lambda df: not df.empty, map(_map, df_list)))
                if len(df_list) > 0:
                    df_dict.setdefault(key, []).append(df_list)
        return df_dict

    def _do_parse_df(self, df_dict: Dict[str, List[List[DataFrame]]],
                     attribute_manager: AttributeManager) -> List[DataFrame]:
        client_code_column = attribute_manager.value(attr_string.client_code_column)
        money_column = attribute_manager.value(attr_string.money_column)
        rate_column = attribute_manager.value(attr_string.rate_column)
        kind_column = attribute_manager.value(attr_string.kind_column)
        use_column = attribute_manager.value(attr_string.use_column)
        qty_column = attribute_manager.value(attr_string.qty_column)

        def _qty(row):
            u = row[use_column]
            if u == "染费":
                return 0
            else:
                return row[qty_column]

        no = 0
        df_result_list: typing.List[DataFrame] = []
        for key_time in df_dict:
            for df_list in df_dict[key_time]:
                for df in df_list:
                    no = no + 1
                    # 序号
                    df[self.add_no] = no
                    # 开票日期
                    df[self.add_date] = key_time
                    # 客户编码 + 序号
                    df[self.add_code] = df[client_code_column] + "-" + str(no)
                    # 开票日期1
                    df[self.add_date_1] = key_time
                    # 主营业收入
                    df[self.add_money] = df[money_column]
                    # 税额
                    df[self.add_tax] = df[money_column] * df[rate_column]
                    # 开票日期
                    df[self.add_tax_money] = df[self.add_money] + df[self.add_tax]
                    # 入库数量
                    df[self.add_qty] = df.apply(func=_qty, axis=1)
                    # 类别
                    df[self.add_kind] = df[kind_column] + df[use_column]

                    df_result_list.append(df)

        return [pd.concat(df_result_list)]

    def _do_reset_index(self, df_list: List[DataFrame], attribute_manager: AttributeManager):
        DefaultResetIndex().reset_index(df_list, attribute_manager)

    def _do_create_describe_4_excel(self, df_list: List[DataFrame],
                                    attribute_manager: AttributeManager) -> List[DescribeExcel]:
        return DefaultCreateDescribe4Excel().create_describe_4_excel(df_list=df_list,
                                                                     attribute_manager=attribute_manager)

    def _do_write_excel(self, describe_excel_list: List[DescribeExcel], attribute_manager: AttributeManager,
                        target_file: str):
        DefaultWriteExcel().write_excel(describe_excel_list, attribute_manager, target_file)

    def _do_render_target(self, describe_excel_list: List[DescribeExcel], attribute_manager: AttributeManager,
                          target_file: str):
        DefaultRender().render(describe_excel_list=describe_excel_list,
                               attribute_manager=attribute_manager,
                               target_file=target_file)
