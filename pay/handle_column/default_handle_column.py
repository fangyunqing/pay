# @Time    : 23/02/09 8:45
# @Author  : fyq
# @File    : default_handle_column.py
# @Software: PyCharm

__author__ = 'fyq'

import typing


from pandas import DataFrame

from pay.attribute import AttributeManager
from pay.handle_column.handle_column import HandleColumn


class DefaultHandleColumn(HandleColumn):

    """
        只是把float的保留两位小数
    """
    def handle_column(self, df_list: typing.List[DataFrame], attribute_manager: AttributeManager):
        for df in df_list:
            for type_index, type_value in list(df.dtypes.items()):
                if "float" in type_value.name:
                    df[type_index] = df[type_index].apply(lambda c: round(c, 2))
