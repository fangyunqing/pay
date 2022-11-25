# @Time    : 22/11/15 10:50
# @Author  : fyq
# @File    : abstract_reconciliation_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import abstractmethod

from pay.create_describe_4_excel.reconciliation_create_describe_4_excel import ReconciliationCreateDescribe4Excel
from pay.file_parser.map.abstract_map_file_parser import AbstractMapFileParser
from pay.render.default_render import DefaultRender
from pay.reset_index.default_reset_index import DefaultResetIndex
from pay.write_excel.default_write_excel import DefaultWriteExcel
import pandas as pd
import pay.constant as pc
from util import remove_zero


class AbstractReconciliationFileParser(AbstractMapFileParser):

    @abstractmethod
    def _after_parse_map(self, df, attribute_manager):
        """

        :param df:
        :param attribute_manager:
        :return: ([df, (group list)])
        """
        pass

    @abstractmethod
    def _doing_parse_map(self, file_dict, attribute_manager):
        pass

    @abstractmethod
    def _after_parse_data(self, df, attribute_manager):
        pass

    @abstractmethod
    def _doing_parse_data(self, file_dict, attribute_manager):
        pass

    @abstractmethod
    def _after_merger(self, df_list, attribute_manager):
        pass

    @abstractmethod
    def _before_merger(self, map_df_info_list, data_df, attribute_manager):
        pass

    @abstractmethod
    def _doing_merger(self, map_df_info, data_df, attribute_manager):
        pass

    def _do_parse_map(self, file_dict, attribute_manager):
        df = self._doing_parse_map(file_dict=file_dict, attribute_manager=attribute_manager)
        df_info_list = self._after_parse_map(df=df, attribute_manager=attribute_manager)
        for df_info in df_info_list:
            if not callable(df_info[0]):
                df_info[0].dropna(inplace=True)
                df_info[0][pc.new_bill_code] = df_info[0][pc.new_bill_code].astype("str")
                df_info[0][pc.new_bill_code] = df_info[0][pc.new_bill_code].apply(lambda x: x.strip().replace("'", ""))
        return df_info_list

    def _do_parse_data(self, file_dict, attribute_manager):
        df = self._doing_parse_data(file_dict=file_dict, attribute_manager=attribute_manager)
        df = self._after_parse_data(df=df, attribute_manager=attribute_manager)
        df[pc.new_bill_code] = df[pc.new_bill_code].astype("str")
        df[pc.new_bill_code] = df[pc.new_bill_code].apply(lambda x: x.strip().replace("'", ""))
        return df

    def _do_merger(self, map_df_info_list, data_df, attribute_manager):
        self._before_merger(map_df_info_list, data_df, attribute_manager)
        df_collect_list = []
        df_result_list = []
        df_not_found = []
        df_total_list = []
        df_list = []
        for map_df_index, map_df_info in enumerate(map_df_info_list):
            map_df, search_column_list = map_df_info
            if map_df_index == 0 or not callable(map_df):
                df_collect_list.append(self._doing_merger(map_df_info=map_df_info,
                                                          data_df=data_df,
                                                          attribute_manager=attribute_manager))
            elif callable(map_df):
                df_collect_list.append(self._doing_merger(map_df_info=[map_df(df_collect_list[map_df_index-1][1]),
                                                                       search_column_list],
                                                          data_df=data_df,
                                                          attribute_manager=attribute_manager))

        for df_collect in df_collect_list:
            df_result, df_not_found, df_total = df_collect
            data_bill_code = attribute_manager.value(pc.data_bill_code)
            df_result[data_bill_code] = df_result[data_bill_code].apply(remove_zero)
            df_result_list.append(df_result)
            df_total_list.append(df_total)
        df_list.append(pd.concat(df_result_list)) if len(df_result_list) > 1 else df_list.append(df_result_list[0])
        df_list.append(df_not_found)
        df_list.append(pd.concat(df_total_list)) if len(df_total_list) > 1 else df_list.append(df_total_list[0])
        self._after_merger(df_list=df_list, attribute_manager=attribute_manager)
        return df_list

    def _do_reset_index(self, df, attribute_manager):
        DefaultResetIndex().reset_index(df, attribute_manager)

    def _do_create_describe_4_excel(self, df, attribute_manager):
        return ReconciliationCreateDescribe4Excel().create_describe_4_excel(df_list=df,
                                                                            attribute_manager=attribute_manager)

    def _do_write_excel(self, describe_excel, attribute_manager, target_file):
        DefaultWriteExcel().write_excel(describe_excel, attribute_manager, target_file)

    def _do_render_target(self, describe_excel_list, attribute_manager, target_file):
        DefaultRender().render(describe_excel_list, attribute_manager, target_file)

