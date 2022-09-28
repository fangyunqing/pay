# @Time    : 22/09/27 10:40
# @Author  : fyq
# @File    : default_write_excel.py
# @Software: PyCharm

__author__ = 'fyq'


import pandas as pd
from pay.write_excel.write_excel import WriteExcel


class DefaultWriteExcel(WriteExcel):

    def write_excel(self, describe_excel_list, attribute_manager, target_file):
        target_sheet_list = list(pd.read_excel(io=target_file, sheet_name=None))
        with pd.ExcelWriter(target_file,
                            engine='openpyxl',
                            mode='a',
                            if_sheet_exists="overlay") as writer:
            for describe_excel in describe_excel_list:
                for ts in target_sheet_list:
                    if describe_excel.sheet_name == ts.strip():
                        describe_excel.sheet_name = ts
                        break
                describe_excel.df.to_excel(writer,
                                           startrow=describe_excel.start_row,
                                           startcol=describe_excel.start_column,
                                           sheet_name=describe_excel.sheet_name,
                                           header=None,
                                           index=None)