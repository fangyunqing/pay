# @Time    : 23/02/09 10:06
# @Author  : fyq
# @File    : invoice_2_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from typing import Dict, List, Iterable

import typing
from pandas import DataFrame
from pay.attribute import AttributeManager
from pay.constant import attr_string
from pay.file_parser.invoice import InvoiceFileParser
from util import pd_read_excel_by_path
import pandas as pd
import numpy as np


class Invoice2FileParser(InvoiceFileParser):

    def _do_read_file(self, file_dict: Dict[str, Iterable],
                      attribute_manager: AttributeManager) -> Dict[str, List[List[DataFrame]]]:
        read_sheet = attribute_manager.value(attr_string.read_sheet)
        skip_rows = attribute_manager.value(attr_string.skip_rows)
        skip_text: str = attribute_manager.value(attr_string.skip_text)
        use_column = attribute_manager.value(attr_string.use_columns)
        df_dict: Dict[str, List[List[DataFrame]]] = {}
        skip_text_list: typing.List[str] = []
        if skip_text and len(skip_text) > 0:
            skip_text_list = skip_text.split(",")
        for key in file_dict.keys():
            file_path_list = file_dict[key]
            for file_path in file_path_list:
                df_list = pd_read_excel_by_path(file_path=file_path,
                                                read_sheet=read_sheet,
                                                skip_rows=skip_rows,
                                                use_column=use_column.split(","),
                                                limit=False,
                                                limit_column=0,
                                                limit_value="合计")

                drop_row_list = []
                for df in df_list:
                    df.dropna(inplace=True, how="all")
                    for df_index, df_row in df.iterrows():
                        for c in df.columns:
                            val = str(df_row[c])
                            if any(map(lambda st: st.strip() in val, skip_text_list)):
                                drop_row_list.append(df_index)
                                break
                    if len(drop_row_list) > 0:
                        df.drop(labels=drop_row_list, errors="ignore", inplace=True)
                    df["key"] = key
                if len(df_list) > 0:
                    df_dict.setdefault(key, []).append(df_list)
        return df_dict

    def _do_parse_df(self, df_dict: Dict[str, List[List[DataFrame]]],
                     attribute_manager: AttributeManager) -> List[DataFrame]:

        df_all: typing.List[DataFrame] = []
        for df_name, df_list_list in df_dict.items():
            for df_list in df_list_list:
                df_all = df_all + df_list
        df = pd.concat(df_all)
        drop_row_list = []
        df["no"] = np.nan
        no = 1
        df.index = range(0, len(df.index))
        for df_index, df_row in df.iterrows():
            for c in df.columns:
                val = str(df_row[c])
                if val == "合计":
                    df.loc[df_index, "no"] = no
                    drop_row_list.append(df_index)
                    no = no + 1
                    break
        df.fillna(method="backfill", inplace=True)
        df.drop(labels=drop_row_list, inplace=True, errors="ignore")
        df["no"] = df["no"].astype(np.int64)
        return [df]
