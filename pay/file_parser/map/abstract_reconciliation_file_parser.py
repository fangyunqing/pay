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


class AbstractReconciliationFileParser(AbstractMapFileParser):

    @abstractmethod
    def _after_parse_map(self, df, attribute_manager):
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
    def _doing_merger(self, map_df, data_df, attribute_manager):
        pass

    def _do_parse_map(self, file_dict, attribute_manager):
        df = self._doing_parse_map(file_dict=file_dict, attribute_manager=attribute_manager)
        df = self._after_parse_map(df=df, attribute_manager=attribute_manager)
        df.dropna(inplace=True)
        return df

    def _do_parse_data(self, file_dict, attribute_manager):
        df = self._doing_parse_data(file_dict=file_dict, attribute_manager=attribute_manager)
        df = self._after_parse_data(df=df, attribute_manager=attribute_manager)
        return df

    def _do_merger(self, map_df, data_df, attribute_manager):
        df_list = self._doing_merger(map_df=map_df, data_df=data_df, attribute_manager=attribute_manager)
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

