# @Time    : 22/09/27 9:32
# @Author  : fyq
# @File    : reconciliation_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.file_parser.map.abstract_reconciliation_file_parser import AbstractReconciliationFileParser
from pay.reset_index.default_reset_index import DefaultResetIndex
from pay.create_describe_4_excel.reconciliation_create_describe_4_excel import ReconciliationCreateDescribe4Excel
from pay.write_excel.default_write_excel import DefaultWriteExcel
import pay.constant as pc
import pandas as pd
from pay.handle_parser.default_handle_parser import DefaultHandleParser
from pay.render.default_render import DefaultRender
from util import remove_zero


class ReconciliationFileParser(AbstractReconciliationFileParser):
    """
        普通应收对账 通过订单号查询
    """

    def _before_merger(self, map_df_info_list, data_df, attribute_manager):
        pass

    def _after_parse_map(self, df, attribute_manager):
        map_bill_code = attribute_manager.value(pc.map_bill_code)
        df[pc.new_bill_code] = df[map_bill_code]
        return [df, [pc.new_bill_code]]

    def _doing_parse_map(self, file_dict, attribute_manager):
        map_file_info = str(attribute_manager.value(pc.map_file)).split(",")
        map_use_column_list = list(attribute_manager.value(pc.map_use_column).split(","))
        map_df = DefaultHandleParser().handle_parser(file_dict=file_dict,
                                                     file_info=map_file_info,
                                                     use_column_list=map_use_column_list,
                                                     attribute_manager=attribute_manager)
        return map_df

    def _after_parse_data(self, df, attribute_manager):
        data_bill_code = attribute_manager.value(pc.data_bill_code)
        df[pc.new_bill_code] = df[data_bill_code]
        return df

    def _doing_parse_data(self, file_dict, attribute_manager):
        data_file_info = str(attribute_manager.value(pc.data_file)).split(",")
        data_use_column_list = list(attribute_manager.value(pc.data_use_column).split(","))
        data_df = DefaultHandleParser().handle_parser(file_dict=file_dict,
                                                      file_info=data_file_info,
                                                      use_column_list=data_use_column_list,
                                                      attribute_manager=attribute_manager)
        return data_df

    def _after_merger(self, df_list, attribute_manager):
        return df_list

    def _doing_merger(self, map_df_info, data_df, attribute_manager):
        # unpack
        map_df, search_column_list = map_df_info
        self._modify_attribute_manager(map_df, data_df, attribute_manager)
        map_bill_code = attribute_manager.value(pc.map_bill_code)
        map_data_list = list(attribute_manager.value(pc.map_data).split(","))
        df_list = []
        df_not_found_list = []
        s_total_list = []

        for map_unique in search_column_list:
            map_df[map_unique] = map_df[map_unique].astype("str", errors="ignore").apply(remove_zero)

        for data_unique in search_column_list:
            data_df[data_unique] = data_df[data_unique].astype("str", errors="ignore").apply(remove_zero)

        for ri, r in map_df.iterrows():

            df = data_df
            for search_column in search_column_list:
                df = df.loc[df[search_column] == r[search_column]]

            if len(df.index) == 0:
                df_not_found_list.append(r.to_frame().T)
                continue

            # 删除已经找到的数据
            data_df.drop(labels=df.index, inplace=True)

            self._doing_merger_modify(map_df_row=r,
                                      data_df=df,
                                      attribute_manager=attribute_manager)

            map_diff_list = []
            data_diff_list = []

            s_total = pd.Series(index=search_column_list)
            s_total_list.append(s_total)
            for map_unique in search_column_list:
                s_total.loc[map_unique] = r[map_unique]

            for i, map_data in enumerate(map_data_list):
                map_diff, data_diff, diff_type = map_data.split(":")
                map_diff_list.append(map_diff)
                data_diff_list.append(data_diff)
                diff_column = "diff" + str(i)

                if diff_type == "0":
                    df[diff_column] = ""
                    s_diff = df[data_diff] == r[map_diff]
                    s_total.loc[data_diff] = ",".join([str(s) for s in df[data_diff].unique().tolist()])
                    s_total.loc[map_diff + "-1"] = r[map_diff]
                    if not s_diff.all():
                        first_row = df.iloc[0]
                        first_row[diff_column] = r[map_diff]
                        df.iloc[0] = first_row
                else:
                    df[diff_column] = ""
                    df[diff_column + "-1"] = ""
                    data_sum = round(df[data_diff].sum(), 6)
                    map_sum = round(r[map_diff], 6)
                    diff = round(map_sum - data_sum, 6)
                    s_total.loc[data_diff] = data_sum
                    s_total.loc[map_diff + "-1"] = map_sum
                    s_total.loc[data_diff + "-" + map_diff] = 0
                    if abs(diff) != 0:
                        s_total.loc[data_diff + "-" + map_diff] = diff
                        first_row = df.iloc[0]
                        first_row[diff_column] = map_sum
                        first_row[diff_column + "-1"] = diff
                        df.iloc[0] = first_row
            df_list.append(df)
        df_total = None
        if len(s_total_list) > 0:
            df_total = pd.concat(s_total_list, axis=1, ignore_index=False).T
        df_list = [pd.concat(df_list) if len(df_list) > 0 else None,
                   pd.concat(df_not_found_list) if len(df_not_found_list) > 0 else None,
                   df_total]
        return df_list

    def _modify_attribute_manager(self, map_df, data_df, attribute_manager):
        pass

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
        return "常用" == pay_type

    def _doing_merger_modify(self, map_df_row, data_df, attribute_manager):
        pass
