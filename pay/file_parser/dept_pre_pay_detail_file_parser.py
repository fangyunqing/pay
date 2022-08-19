# @Time    : 22/08/17 10:03
# @Author  : fyq
# @File    : dept_pre_pay_detail_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.file_parser.abstract_default_file_parser import AbstractDefaultFileParser
import pay.constant as pc
import pandas as pd


class DeptPrePayDetailFileParser(AbstractDefaultFileParser):

    def _do_parse_df_dict(self, df_dict, attribute_manager):
        supplier_column = attribute_manager.value(pc.supplier_column)
        pur_group_column = attribute_manager.value(pc.pur_group)
        pur_no_column = attribute_manager.value(pc.pur_no)
        type_column = attribute_manager.value(pc.type_column)
        pre_pay_column = [int(c) for c in attribute_manager.value(pc.pre_pay).split(",")]
        pre_pay_column.sort()
        df_list = []
        for key in df_dict.keys():
            df = df_dict[key]
            df.sort_values(attribute_manager.value(pc.sort_column), ascending=False, inplace=True)
            df_list.append(df)
        df_detail = pd.concat(df_list)
        # 计算合计
        df_total = df_detail.sum(numeric_only=True).to_frame().T
        df_total.insert(column=pur_no_column, value="", loc=0)
        df_total.insert(column=supplier_column, value="合计", loc=0)
        df_total.insert(column=pur_group_column, value="", loc=0)
        df_total.insert(column=type_column, value="", loc=0)
        for c in pre_pay_column:
            df_total[str(c)] = ""
        return [pd.concat([df_total, df_detail])]

    def _group_column(self, attribute_manager):
        return [attribute_manager.value(pc.supplier_column),
                attribute_manager.value(pc.type_column),
                attribute_manager.value(pc.pur_group),
                attribute_manager.value(pc.pur_no),
                *attribute_manager.value(pc.pre_pay).split(",")]

    def __init__(self):
        super().__init__()
        self._insert_name = False

    def support(self, pay_type):
        return pay_type == "dept.pre_pay_detail"
