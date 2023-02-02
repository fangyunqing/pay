# @Time    : 22/08/15 14:53
# @Author  : fyq
# @File    : group_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from typing import Dict, Iterable, List

from pandas import DataFrame

from pay.attribute import AttributeManager
import pay.constant as pc
import pandas as pd
import yaml

from pay.file_parser.payable.abstract_common_payable_file_parser import AbstractCommonPayableFileParser


class GroupFileParser(AbstractCommonPayableFileParser):

    def _insert_name(self) -> bool:
        return True

    def _do_parse_df(self, df_dict: Dict[str, DataFrame], attribute_manager: AttributeManager) -> List[DataFrame]:
        type_column = attribute_manager.value(pc.type_column)
        supplier_column = attribute_manager.value(pc.supplier_column)
        for key in df_dict.keys():
            df = df_dict[key]
            # 去除supplier列
            df.drop([supplier_column], axis=1, inplace=True, errors="ignore")
            # 根据dept和type统计
            df = df.groupby([self._name_column, type_column], as_index=False).sum()
            # 根据dept统计
            df_total = df.groupby([self._name_column], as_index=False).sum()
            df_total.insert(column=type_column, value="合计", loc=1)
            # 替换
            df_dict[key] = pd.concat([df_total, df])
            # 排序
            df_dict[key].sort_values(attribute_manager.value(pc.sort_column), ascending=False, inplace=True)

        real_df_list, df = self._split_dept(value=yaml.safe_load(attribute_manager.value(pc.dept).replace("yaml", "")),
                                            df_dict=df_dict,
                                            attribute_manager=attribute_manager)
        return [df]

    def _ignore_not_exist(self) -> bool:
        return False

    def _first_column_merger(self) -> int:
        return 1

    def support(self, pay_type):
        return True

    def _group_column(self, attribute_manager):
        return [attribute_manager.value(pc.supplier_column),
                attribute_manager.value(pc.type_column)]

    def _split_dept(self, value, df_dict, attribute_manager):
        type_column = attribute_manager.value(pc.type_column)
        if isinstance(value, str):
            return df_dict.get(value)
        elif isinstance(value, dict):
            df_all = None
            real_df_all_list = []
            for k in value.keys():
                real_df_list, df = self._split_dept(value[k], df_dict, attribute_manager=attribute_manager)
                if len(real_df_list) > 0:
                    real_df_all_list.extend(real_df_list)
                    df_sum = pd.concat(real_df_list).groupby([type_column], as_index=False).sum()
                    df_sum.insert(column=self._name_column, value=k, loc=0)
                    df_sum.sort_values(attribute_manager.value(pc.sort_column), ascending=False, inplace=True)
                    if df_all is None:
                        df_all = pd.concat([df_sum, df])
                    else:
                        df_all = pd.concat[[df_all, df_sum, df, df]]
            return real_df_all_list, df_all
        elif isinstance(value, list):
            df_list = []
            real_df_list = []
            for k in value:
                rs = self._split_dept(k, df_dict, attribute_manager=attribute_manager)
                if isinstance(rs, (tuple, list)):
                    real_df_list.extend(rs[0])
                    df_list.append(rs[1])
                elif rs is not None:
                    real_df_list.append(rs)
                    df_list.append(rs)
            df_list = list(filter(lambda val: val is not None, df_list))
            real_df_list = list(filter(lambda val: val is not None, real_df_list))
            return real_df_list, pd.concat(df_list) if len(df_list) > 0 else None
