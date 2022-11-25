# @Time    : 22/08/12 16:06
# @Author  : fyq
# @File    : abstract_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.file_parser.file_parser import FileParser
import pandas as pd
import pay.constant as pc
from abc import abstractmethod


class AbstractFileParser(FileParser):

    def parse_file(self, file_dict, target_file, attribute_manager):
        pd.set_option('display.max_columns', None)
        # 解析文件
        df_dict = self._parser_file_dict(file_dict=file_dict,
                                         attribute_manager=attribute_manager,
                                         ignore=self._ignore())
        # 解析df
        df_parse_list = self._parse_df_dict(df_dict=df_dict,
                                            attribute_manager=attribute_manager)
        # 索引重建
        self._reset_index(df_parse_list=df_parse_list,
                          attribute_manager=attribute_manager)
        # 效对
        self._check(df_parse_list=df_parse_list,
                    attribute_manager=attribute_manager)
        # 描述
        describe_excel_list = self._create_describe_4_excel(df_parse_list=df_parse_list,
                                                            attribute_manager=attribute_manager)
        # 写入excel
        self._write_excel(describe_excel_list=describe_excel_list,
                          attribute_manager=attribute_manager,
                          target_file=target_file)
        # 渲染
        self._render_target(describe_excel_list=describe_excel_list,
                            attribute_manager=attribute_manager,
                            target_file=target_file)

    @abstractmethod
    def _parser_file_dict(self, file_dict, attribute_manager, ignore):
        pass

    @abstractmethod
    def _parse_df_dict(self, df_dict, attribute_manager):
        pass

    @abstractmethod
    def _reset_index(self, df_parse_list, attribute_manager):
        pass

    @abstractmethod
    def _check(self, df_parse_list, attribute_manager):
        pass

    @abstractmethod
    def _create_describe_4_excel(self, df_parse_list, attribute_manager):
        pass

    @abstractmethod
    def _write_excel(self, describe_excel_list, attribute_manager, target_file):
        pass

    @abstractmethod
    def _render_target(self, describe_excel_list, attribute_manager, target_file):
        pass

    @abstractmethod
    def _ignore(self):
        pass
