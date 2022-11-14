# @Time    : 22/11/11 15:03
# @Author  : fyq
# @File    : abstract_check_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'


from abc import abstractmethod

from pay.decorator.pay_log import PayLog
from pay.file_parser.file_parser import FileParser


class AbstractCheckFileParser(FileParser):

    def parse_file(self, file_dict, target_file, attribute_manager):
        # 解析文件
        df_list = self._parse_data(file_dict, target_file, attribute_manager)
        # 重建索引
        self._reset_index(df_list, attribute_manager)
        # excel描述符
        describe_excel = self._create_describe_4_excel(df_list, attribute_manager)
        # 写入excel
        self._write_excel(describe_excel, attribute_manager, target_file)
        # 渲染excel
        self._render_target(describe_excel, attribute_manager, target_file)

    @PayLog(node="解析文件")
    def _parse_data(self, file_dict, target_file, attribute_manager):
        return self._do_parse_data(file_dict, target_file, attribute_manager)

    @abstractmethod
    def _do_parse_data(self, file_dict, target_file, attribute_manager):
        pass

    @PayLog(node="创建excel文件描述")
    def _create_describe_4_excel(self, df, attribute_manager):
        return self._do_create_describe_4_excel(df, attribute_manager)

    @abstractmethod
    def _do_create_describe_4_excel(self, df, attribute_manager):
        pass

    @PayLog(node="写入excel")
    def _write_excel(self, describe_excel, attribute_manager, target_file):
        self._do_write_excel(describe_excel, attribute_manager, target_file)

    @abstractmethod
    def _do_write_excel(self, describe_excel, attribute_manager, target_file):
        pass

    @PayLog(node="渲染excel")
    def _render_target(self, describe_excel_list, attribute_manager, target_file):
        self._do_render_target(describe_excel_list, attribute_manager, target_file)

    @abstractmethod
    def _do_render_target(self, describe_excel, attribute_manager, target_file):
        pass

    @PayLog(node="重建索引")
    def _reset_index(self, df, attribute_manager):
        self._do_reset_index(df, attribute_manager)

    @abstractmethod
    def _do_reset_index(self, df, attribute_manager):
        pass
