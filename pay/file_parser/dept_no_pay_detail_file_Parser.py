# @Time    : 22/08/17 10:13
# @Author  : fyq
# @File    : dept_no_pay_detail_file_Parser.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.file_parser.abstract_default_file_parser import AbstractDefaultFileParser
import pay.constant as pc
import pandas as pd


class DeptNoPayDetailFileParser(AbstractDefaultFileParser):

    def support(self, pay_type):
        return pay_type == "dept.no_pay_detail"

    def _do_parse_df_dict(self, df_dict, attribute_manager):
        supplier_column = attribute_manager.value(pc.supplier_column)
        pur_group_column = attribute_manager.value(pc.pur_group)
        type_column = attribute_manager.value(pc.type_column)
        no_pay_reason_column = [int(c) for c in attribute_manager.value(pc.no_pay_reason).split(",")]
        no_pay_reason_column.sort()
        df_list = []
        for key in df_dict.keys():
            df = df_dict[key]
            df.sort_values(attribute_manager.value(pc.sort_column), ascending=False, inplace=True)
            df_list.append(df)
        df_detail = pd.concat(df_list)
        # 去未请款说明 供应商列 组织列
        df_little_total = df_detail.drop([supplier_column, pur_group_column, *no_pay_reason_column],
                                         axis=1,
                                         errors="ignore").groupby([type_column],
                                                                  as_index=False).sum()
        for gc in no_pay_reason_column:
            df_little_total[str(gc)] = ""
        df_little_total.insert(column=supplier_column, value="小计", loc=1)
        df_little_total.insert(column=pur_group_column, value="", loc=1)

        df_total = df_detail.sum(numeric_only=True).to_frame().T
        for gc in no_pay_reason_column:
            df_total[str(gc)] = ""
        df_total.insert(column=supplier_column, value="小计", loc=0)
        df_total.insert(column=pur_group_column, value="", loc=0)
        df_total.insert(column=type_column, value="", loc=0)
        return [pd.concat([df_total, df_little_total, df_detail])]

    def _group_column(self, attribute_manager):
        return [attribute_manager.value(pc.supplier_column),
                attribute_manager.value(pc.type_column),
                attribute_manager.value(pc.pur_group),
                *attribute_manager.value(pc.no_pay_reason).split(",")]

    def __init__(self):
        super().__init__()
        self._insert_name = False
