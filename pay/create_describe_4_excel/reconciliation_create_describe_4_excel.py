# @Time    : 22/09/27 16:48
# @Author  : fyq
# @File    : reconciliation_create_describe_4_excel.py
# @Software: PyCharm

__author__ = 'fyq'


from pay.create_describe_4_excel.default_create_describe_4_excel import DefaultCreateDescribe4Excel
import pay.constant as pc
from pay.entity.describe_excel.map_describe_excel import MapDescribeExcel


class ReconciliationCreateDescribe4Excel(DefaultCreateDescribe4Excel):

    def write_sheet_list(self, attribute_manager):
        write_sheet_list = super(ReconciliationCreateDescribe4Excel, self).write_sheet_list(attribute_manager)
        write_sheet_list.append(attribute_manager.value(pc.write_not_found_sheet))
        write_sheet_list.append(attribute_manager.value(pc.write_total_sheet))
        return write_sheet_list

    # def create_describe_4_excel(self, df_list, attribute_manager):
    #     write_sheet_list = self.write_sheet_list(attribute_manager)
    #     describe_excel_list = []
    #     for index, df in enumerate(df_list):
    #         if len(write_sheet_list) - 1 >= index:
    #             write_sheet = write_sheet_list[index]
    #         else:
    #             write_sheet = write_sheet_list[len(write_sheet_list) - 1]
    #         write_sheet_info = list(write_sheet.split(","))
    #         describe_excel = MapDescribeExcel()
    #         describe_excel.df = df
    #         describe_excel.row = len(df.index)
    #         describe_excel.column = len(df.columns)
    #         describe_excel.sheet_name = write_sheet_info[0]
    #         describe_excel.start_row = int(write_sheet_info[1])
    #         describe_excel.start_column = int(write_sheet_info[2])
    #         describe_excel_list.append(describe_excel)
    #
    #     return describe_excel_list
