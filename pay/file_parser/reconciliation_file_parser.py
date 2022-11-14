# @Time    : 22/09/27 9:32
# @Author  : fyq
# @File    : reconciliation_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.file_parser.abstract_map_file_parser import AbstractMapFileParser
from pay.reset_index.default_reset_index import DefaultResetIndex
from pay.create_describe_4_excel.reconciliation_create_describe_4_excel import ReconciliationCreateDescribe4Excel
from pay.write_excel.default_write_excel import DefaultWriteExcel
import pay.constant as pc
import pandas as pd
from pay.handle_parser.default_handle_parser import DefaultHandleParser
from pay.render.default_render import DefaultRender


class ReconciliationFileParser(AbstractMapFileParser):

    def _do_parse_map(self, file_dict, attribute_manager):
        map_file_info = str(attribute_manager.value(pc.map_file)).split(",")
        map_use_column_list = list(attribute_manager.value(pc.map_use_column).split(","))
        map_df = DefaultHandleParser().handle_parser(file_dict=file_dict,
                                                     file_info=map_file_info,
                                                     use_column_list=map_use_column_list,
                                                     attribute_manager=attribute_manager)
        map_df.dropna(inplace=True)
        return map_df

    def _do_parse_data(self, file_dict, attribute_manager):
        data_file_info = str(attribute_manager.value(pc.data_file)).split(",")
        data_use_column_list = list(attribute_manager.value(pc.data_use_column).split(","))
        return DefaultHandleParser().handle_parser(file_dict=file_dict,
                                                   file_info=data_file_info,
                                                   use_column_list=data_use_column_list,
                                                   attribute_manager=attribute_manager)

    def _do_merger(self, map_df, data_df, attribute_manager):
        map_bill_code = attribute_manager.value(pc.map_bill_code)
        data_bill_code = attribute_manager.value(pc.data_bill_code)
        map_data_list = list(attribute_manager.value(pc.map_data).split(","))
        df_list = []
        df_not_found_list = []
        for ri, r in map_df.iterrows():
            df = data_df.loc[data_df[data_bill_code] == r[map_bill_code]]
            if len(df.index) == 0:
                df_not_found_list.append(r.to_frame().T)
                continue
            map_diff_list = []
            data_diff_list = []
            for i, map_data in enumerate(map_data_list):
                map_diff, data_diff, diff_type = map_data.split(":")
                map_diff_list.append(map_diff)
                data_diff_list.append(data_diff)
                diff_column = "diff" + str(i)

                if diff_type == "0":
                    df[diff_column] = ""
                    s_diff = df[data_diff] == r[map_diff]
                    if not s_diff.all():
                        first_row = df.iloc[0]
                        first_row[diff_column] = r[map_diff]
                        df.iloc[0] = first_row
                else:
                    df[diff_column] = ""
                    df[diff_column + "-1"] = ""
                    data_sum = round(df[data_diff].sum(), 6)
                    if data_sum != r[map_diff]:
                        first_row = df.iloc[0]
                        first_row[diff_column] = r[map_diff]
                        first_row[diff_column + "-1"] = r[map_diff] - data_sum
                        df.iloc[0] = first_row
            df_list.append(df)
        return [pd.concat(df_list) if len(df_list) > 0 else None,
                pd.concat(df_not_found_list) if len(df_not_found_list) > 0 else None]

    def _do_reset_index(self, df, attribute_manager):
        DefaultResetIndex().reset_index(df, attribute_manager)

    def _do_create_describe_4_excel(self, df, attribute_manager):
        return ReconciliationCreateDescribe4Excel().create_describe_4_excel(df_list=df,
                                                                            attribute_manager=attribute_manager)

    def _do_write_excel(self, describe_excel, attribute_manager, target_file):
        DefaultWriteExcel().write_excel(describe_excel, attribute_manager, target_file)

    def _do_render_target(self, describe_excel_list, attribute_manager, target_file):
        DefaultRender().render(describe_excel_list, attribute_manager, target_file)

    def support(self, pay_type):
        return "单一"
