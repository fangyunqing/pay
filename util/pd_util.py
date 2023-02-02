# @Time    : 22/11/11 15:56
# @Author  : fyq
# @File    : pd_util.py
# @Software: PyCharm

__author__ = 'fyq'

import pandas as pd
import typing

from pandas import DataFrame,Series


def pd_read_excel(file_info, file_dict, use_column, data_type=None):
    """
        读取excel
    :param data_type:
    :param file_info: 文件名, 工作簿, 跳过的行数
    :param file_dict:
    :param use_column:
    :return:
    """

    file_name, sheet_name, skip_row = file_info
    sheet_name = sheet_name.strip()
    if file_name not in file_dict.keys():
        raise Exception("[%s]文件中未找到" % file_name)
    # 读取文件
    file_path = file_dict[file_name][0]
    df_read_dict = pd.read_excel(io=file_path,
                                 sheet_name=None,
                                 skiprows=int(skip_row),
                                 header=None,
                                 dtype=data_type)
    df = None
    for sn in df_read_dict.keys():
        if sn.strip() == sheet_name.strip():
            df = df_read_dict[sn]
            break

    if df is None:
        raise Exception("[%s]中无法找工作簿[%s]" % (file_name, sheet_name))

    # 去除无用的列
    df.columns = [str(column) for column in df.columns]
    useless_column = []
    for value in df.columns:
        if value not in use_column:
            useless_column.append(value)
    if len(useless_column) > 0:
        df.drop(useless_column, axis=1, inplace=True, errors="ignore")
    return df


def pd_read_excel_by_path(file_path: str,
                          read_sheet: str,
                          skip_rows: int,
                          use_column: typing.List[str],
                          limit: bool,
                          limit_value: str,
                          limit_column: typing.Union[str, int]) -> typing.List[DataFrame]:
    df_read_dict = pd.read_excel(io=file_path,
                                 sheet_name=None,
                                 skiprows=int(skip_rows),
                                 header=None)
    df_list: typing.List[DataFrame] = []
    for sn in df_read_dict.keys():
        if str(sn).strip().startswith(read_sheet.strip()):
            df_list.append(df_read_dict[sn])

    if len(df_list) == 0:
        raise Exception("[%s]中无法找工作簿[%s]" % (file_path, read_sheet))

    if limit:
        new_df_list: typing.List[DataFrame] = []
        for df in df_list:
            s_list: typing.List[Series] = []
            for row_index, row in df.iterrows():
                val = str(row[limit_column]).replace(" ", "")
                if val == limit_value:
                    break
                else:
                    s_list.append(row)
            if len(s_list) > 0:
                new_df_list.append(pd.concat(s_list, axis=1).T)
        df_list = new_df_list
    for df in df_list:
        df.columns = [str(column) for column in df.columns]
        useless_column = []
        for value in df.columns:
            if value not in use_column:
                useless_column.append(value)
        if len(useless_column) > 0:
            df.drop(useless_column, axis=1, inplace=True, errors="ignore")
    return df_list
