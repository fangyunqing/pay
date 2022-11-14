# @Time    : 22/09/27 13:52
# @Author  : fyq
# @File    : default_handle_parser.py
# @Software: PyCharm

__author__ = 'fyq'


from pay.handle_parser.handle_parser import HandleParser
import pandas as pd


class DefaultHandleParser(HandleParser):

    def handle_parser(self, file_dict, file_info, use_column_list, attribute_manager):
        # 文件是否存在
        if file_info[0] not in file_dict:
            raise Exception("对照文件[%s]中未找到" % file_info[0])
        # 读取文件
        file_name = file_dict[file_info[0]][0]
        df_read_dict = pd.read_excel(io=file_name,
                                     sheet_name=None,
                                     skiprows=int(file_info[2]),
                                     header=None)
        df = None
        for sheet_name in df_read_dict.keys():
            if sheet_name.strip() == file_info[1].strip():
                df = df_read_dict[sheet_name]
                break

        if df is None:
            raise Exception("[%s]中无法找工作簿[%s]" % (file_name, file_info[1]))
        # 去除无用的列
        df.columns = [str(column) for column in df.columns]
        useless_column = []
        for value in df.columns:
            if value not in use_column_list:
                useless_column.append(value)
        if len(useless_column) > 0:
            df.drop(useless_column, axis=1, inplace=True, errors="ignore")
        return df
