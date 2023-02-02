# @Time    : 22/11/09 11:09
# @Author  : fyq
# @File    : abstract_pdf_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import abstractmethod

from pay.decorator.pay_log import PayLog
from pay.file_parser.file_parser import FileParser


class AbstractPdfFileParser(FileParser):

    def parse_file(self, file_dict, target_file, attribute_manager):
        # 解析pdf文件
        df = self._parse_pdf(file_dict, attribute_manager)
        # excel描述符
        describe_excel = self._create_describe_4_excel(df, attribute_manager)
        # 写入excel
        self._write_excel(describe_excel, attribute_manager, target_file)
        # 渲染excel
        self._render_target(describe_excel, attribute_manager, target_file)

    @PayLog(node="解析PDF文件")
    def _parse_pdf(self, file_dict, attribute_manager):
        return self._do_parse_pdf(file_dict, attribute_manager)

    @abstractmethod
    def _do_parse_pdf(self, file_dict, attribute_manager):
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
