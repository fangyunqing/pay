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
        with pd.ExcelWriter(path=target_file,
                            mode="a",
                            if_sheet_exists="overlay") as writer:
            if hasattr(writer, "datetime_format"):
                setattr(writer, "datetime_format", "YYYY-MM-DD")
            elif hasattr(writer, "_datetime_format"):
                setattr(writer, "_datetime_format", "YYYY-MM-DD")

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
