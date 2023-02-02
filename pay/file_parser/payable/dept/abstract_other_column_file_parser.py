# @Time    : 22/11/22 13:55
# @Author  : fyq
# @File    : abstract_other_column_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import abstractmethod
from typing import Dict, List

from pandas import DataFrame

from pay.attribute import AttributeManager
from pay.file_parser.payable.abstract_common_payable_file_parser import AbstractCommonPayableFileParser
import pay.constant as pc
import pandas as pd


class AbstractOtherColumnFileParser(AbstractCommonPayableFileParser):

    def _first_column_merger(self) -> int:
        return 0

    def _do_parse_df(self, df_dict: Dict[str, DataFrame], attribute_manager: AttributeManager) -> List[DataFrame]:
        supplier_column = attribute_manager.value(pc.supplier_column)
        pur_group_column = attribute_manager.value(pc.pur_group)
        type_column = attribute_manager.value(pc.type_column)
        _other_column = self._other_column(attribute_manager=attribute_manager)
        df_list = []
        for key in df_dict.keys():
            df = df_dict[key]
            df.sort_values(attribute_manager.value(pc.sort_column), ascending=False, inplace=True)
            df_list.append(df)
        df_detail = pd.concat(df_list)
        # 其他列 供应商列 组织列
        df_little_total = df_detail.drop([supplier_column, pur_group_column, *_other_column],
                                         axis=1,
                                         errors="ignore").groupby([type_column],
                                                                  as_index=False).sum()
        df_little_total.sort_values(attribute_manager.value(pc.sort_column), ascending=False, inplace=True)
        for gc in _other_column:
            df_little_total[str(gc)] = ""
        df_little_total.insert(column=supplier_column, value="小计", loc=1)
        df_little_total.insert(column=pur_group_column, value="", loc=1)

        df_total = df_detail.sum(numeric_only=True).to_frame().T
        for gc in _other_column:
            df_total[str(gc)] = ""
        df_total.insert(column=supplier_column, value="合计", loc=0)
        df_total.insert(column=pur_group_column, value="", loc=0)
        df_total.insert(column=type_column, value="", loc=0)
        return [pd.concat([df_total, df_little_total, df_detail])]

    def _insert_name(self) -> bool:
        return False

    def __init__(self):
        super().__init__()
        self._insert_name = False

    @abstractmethod
    def _other_column(self, attribute_manager):
        pass


