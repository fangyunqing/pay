# @Time    : 22/11/11 15:56
# @Author  : fyq
# @File    : pd_util.py
# @Software: PyCharm

__author__ = 'fyq'

import pandas as pd


def pd_read_excel(file_info, file_dict, use_column):
    """
        读取excel
    :param file_info: 文件名, 工作簿, 列数
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
                                 header=None)
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
