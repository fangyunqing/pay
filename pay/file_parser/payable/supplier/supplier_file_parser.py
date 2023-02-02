# @Time    : 22/08/13 11:32
# @Author  : fyq
# @File    : supplier_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from typing import Dict, Iterable, List

from pandas import DataFrame

from pay.attribute import AttributeManager
import pay.constant as pc
import pandas as pd

from pay.file_parser.payable.abstract_common_payable_file_parser import AbstractCommonPayableFileParser


class SupplierFileParser(AbstractCommonPayableFileParser):

    def _insert_name(self) -> bool:
        return True

    def _do_parse_df(self, df_dict: Dict[str, DataFrame], attribute_manager: AttributeManager) -> List[DataFrame]:
        type_column = attribute_manager.value(pc.type_column)
        supplier_column = attribute_manager.value(pc.supplier_column)
        df_list = []
        for key in df_dict.keys():
            df = df_dict[key]
            # dept type supplier 分组合计
            df_group = df.groupby([self._name_column, type_column, supplier_column],
                                  as_index=False).sum()
            # 排序
            df.sort_values(attribute_manager.value(pc.sort_column), ascending=False, inplace=True)
            # 加入队列
            df_list.append(df_group)
        # 明细
        df_detail_total = pd.concat(df_list)
        df_top_detail_total = df_detail_total.drop([self._name_column, type_column, supplier_column],
                                                   axis=1, errors="ignore").sum().to_frame().T
        df_top_detail_total.insert(column=supplier_column, value="", loc=0)
        df_top_detail_total.insert(column=type_column, value="", loc=0)
        df_top_detail_total.insert(column=self._name_column, value="", loc=0)
        # 去除dept列
        df_total = df_detail_total.drop([self._name_column], axis=1, errors="ignore")
        # 根据type和supplier分组合计
        df_total_dict = {}
        df_total_list = []
        df_top_total_list = []
        df_total = df_total.groupby([type_column, supplier_column], as_index=False).sum()
        for type_name in df_total[type_column].unique():
            df_type = df_total[df_total[type_column] == type_name]
            # 根据type分组合计
            df_type_total = df_type.groupby(type_column, as_index=False).sum()
            df_type_total.insert(column=supplier_column, value="", loc=1)
            df_type_total[type_column] = str(type_name) + "汇总"
            df = pd.concat([df_type_total, df_type])
            # 排序
            df.sort_values(attribute_manager.value(pc.sort_column), ascending=False, inplace=True)
            df_total_dict[type_name] = df
            df_type_total[type_column] = type_name
            df_top_total_list.append(df_type_total)
        # 根据supplier分组合计
        df_top_total = pd.concat(df_top_total_list)
        df_top_total[supplier_column] = "小计"
        df_top_total_total = df_top_total.groupby([supplier_column], as_index=False).sum()
        df_top_total_total.insert(column=type_column, value="", loc=0)
        df_top_total_total[supplier_column] = "合计"
        df_top_total.sort_values(attribute_manager.value(pc.sort_column), ascending=False, inplace=True)
        for type_name in df_top_total[type_column]:
            if type_name in df_total_dict.keys():
                df_total_list.append(df_total_dict[type_name])
        df_total = pd.concat([df_top_total_total, df_top_total, pd.concat(df_total_list)])
        return [df_total, pd.concat([df_top_detail_total, df_detail_total])]

    def _ignore_not_exist(self) -> bool:
        return False

    def _first_column_merger(self) -> int:
        return 0

    def support(self, pay_type):
        return True

    def _group_column(self, attribute_manager):
        return [attribute_manager.value(pc.supplier_column),
                attribute_manager.value(pc.type_column)]

