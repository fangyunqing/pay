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
from pay.create_describe_4_excel import DefaultCreateDescribe4Excel, SupplierCreateDescribe4Excel
from pay.create_describe_4_excel.describe_excel import DescribeExcel

from pay.file_parser.invoice.abstract_invoice_file_parser import AbstractInvoiceFileParser
from pay.handle_column import DefaultHandleColumn
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

        透视表
        pivot_subject 科目编码
        pivot_money1  原币借款
        pivot_money2  本币借款
        pivot_qty1    借方数据
        pivot_qty2    货方数据
        pivot_loan1   原币贷款
        pivot_loan2   本币贷款
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

    pivot_no = "pivot_no"

    pivot_subject = "pivot_subject"

    pivot_money1 = "pivot_money1"

    pivot_money2 = "pivot_money2"

    pivot_qty1 = "pivot_qty1"

    pivot_qty2 = "pivot_qty2"

    pivot_loan1 = "pivot_loan1"

    pivot_loan2 = "pivot_loan2"

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
            u = row[kind_column]
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
                    df[self.add_tax] = df[self.add_money] * df[rate_column]
                    # 开票金额
                    df[self.add_tax_money] = round(df[self.add_money], 2) + round(df[self.add_tax], 2)
                    # 入库数量
                    df[self.add_qty] = df.apply(func=_qty, axis=1)
                    # 类别
                    df[self.add_kind] = df[use_column] + df[kind_column]

                    df_result_list.append(df)

        # 结果集
        pd_ret = pd.concat(df_result_list)
        # 通过结果集生成透视表
        no = 0
        df_pivot_list = []
        for ret_index, ret_row in pd_ret.iterrows():
            no = no + 1
            # 第一行
            first_row = pd.Series(dtype=np.float64)
            first_row[self.add_no] = ret_row[self.add_no]
            first_row[self.add_code] = ret_row[self.add_code]
            first_row[client_code_column] = ret_row[client_code_column]
            first_row[self.add_date] = ret_row[self.add_date]
            first_row[self.add_kind] = ret_row[self.add_kind]
            first_row[self.add_money] = ret_row[self.add_money]
            first_row[self.add_tax] = ret_row[self.add_tax]
            first_row[self.add_tax_money] = ret_row[self.add_tax_money]
            first_row[self.add_qty] = ret_row[self.add_qty]
            first_row[self.pivot_no] = no
            first_row[self.pivot_subject] = "11240101"
            first_row[self.pivot_money1] = ret_row[self.add_tax_money]
            first_row[self.pivot_money2] = ret_row[self.add_tax_money]
            first_row[self.pivot_qty1] = np.nan
            first_row[self.pivot_qty2] = ret_row[self.add_qty]
            first_row[self.pivot_loan1] = np.nan
            first_row[self.pivot_loan2] = np.nan
            # 第二行
            second_row = first_row.copy()
            second_row[...] = np.nan
            second_row[self.pivot_no] = no
            second_row[self.pivot_subject] = "60010101"
            second_row[self.pivot_loan1] = ret_row[self.add_money]
            second_row[self.pivot_loan2] = ret_row[self.add_money]
            # 第三行
            three_row = first_row.copy()
            three_row[...] = np.nan
            three_row[self.pivot_no] = no
            three_row[self.pivot_subject] = "2221011501"
            three_row[self.pivot_loan1] = ret_row[self.add_tax]
            three_row[self.pivot_loan2] = ret_row[self.add_tax]
            # 合并
            df = pd.concat([first_row, second_row, three_row], axis=1).T
            df[self.add_money] = df[self.add_money].astype(np.float64)
            df[self.add_tax] = df[self.add_tax].astype(np.float64)
            df[self.add_tax_money] = df[self.add_tax_money].astype(np.float64)
            df[self.add_qty] = df[self.add_qty].astype(np.float64)
            df[self.pivot_money1] = df[self.pivot_money1].astype(np.float64)
            df[self.pivot_money2] = df[self.pivot_money2].astype(np.float64)
            df[self.pivot_qty1] = df[self.pivot_qty1].astype(np.float64)
            df[self.pivot_qty2] = df[self.pivot_qty2].astype(np.float64)
            df[self.pivot_loan1] = df[self.pivot_loan1].astype(np.float64)
            df[self.pivot_loan2] = df[self.pivot_loan2].astype(np.float64)

            df_pivot_list.append(df)

        return [pd_ret, pd.concat(df_pivot_list)]

    def _do_reset_index(self, df_list: List[DataFrame], attribute_manager: AttributeManager):
        DefaultResetIndex().reset_index(df_list, attribute_manager)

    def _do_create_describe_4_excel(self, df_list: List[DataFrame],
                                    attribute_manager: AttributeManager) -> List[DescribeExcel]:
        return SupplierCreateDescribe4Excel().create_describe_4_excel(df_list=df_list,
                                                                      attribute_manager=attribute_manager)

    def _do_write_excel(self, describe_excel_list: List[DescribeExcel], attribute_manager: AttributeManager,
                        target_file: str):
        DefaultWriteExcel().write_excel(describe_excel_list, attribute_manager, target_file)

    def _do_render_target(self, describe_excel_list: List[DescribeExcel], attribute_manager: AttributeManager,
                          target_file: str):
        DefaultRender().render(describe_excel_list=describe_excel_list,
                               attribute_manager=attribute_manager,
                               target_file=target_file)

    def _do_handle_column(self, df_list: List[DataFrame], attribute_manager: AttributeManager):
        DefaultHandleColumn().handle_column(df_list=df_list, attribute_manager=attribute_manager)
