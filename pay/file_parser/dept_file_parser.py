# @Time    : 22/08/16 14:32
# @Author  : fyq
# @File    : dept_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.file_parser.abstract_default_file_parser import AbstractDefaultFileParser
import pay.constant as pc
import pandas as pd


class DeptFileParser(AbstractDefaultFileParser):

    def support(self, pay_type):
        return pay_type in ("dept.pay", "dept.prepay")

    def __init__(self):
        super().__init__()
        self._insert_name = False

    def _group_column(self, attribute_manager):
        return [attribute_manager.value(pc.supplier_column),
                attribute_manager.value(pc.type_column)]

    def _do_parse_df_dict(self, df_dict, attribute_manager):
        type_column = attribute_manager.value(pc.type_column)
        supplier_column = attribute_manager.value(pc.supplier_column)
        # 分类和供应商分组
        df_total = pd.concat(df_dict.values()).groupby([type_column, supplier_column], as_index=False).sum()
        df_total_dict = {}
        df_top_total_list = []
        df_total_list = []
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
        return [df_total]
