# @Time    : 23/01/31 16:50
# @Author  : fyq
# @File    : abstract_invoice_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import abstractmethod
from typing import Optional, Dict, Iterable, List

from pandas import DataFrame

from pay.attribute import AttributeManager
from pay.create_describe_4_excel.describe_excel import DescribeExcel
from pay.decorator import PayLog
from pay.file_parser.file_parser import FileParser


class AbstractInvoiceFileParser(FileParser):

    def parse_file(self, file_dict: Dict[str, Iterable],
                   target_file: Optional[str], attribute_manager: AttributeManager) -> None:
        # 读取文件
        df_dict = self._read_file(file_dict=file_dict,
                                  attribute_manager=attribute_manager)
        # 解析文件
        df_list = self._parse_df(df_dict=df_dict,
                                 attribute_manager=attribute_manager)
        # 索引重建
        self._reset_index(df_list=df_list,
                          attribute_manager=attribute_manager)

        # 处理列
        self._handle_column(df_list=df_list,
                            attribute_manager=attribute_manager)

        # 创建excel描述符
        describe_excel_list = self._create_describe_4_excel(df_list=df_list,
                                                            attribute_manager=attribute_manager)
        # 写入excel
        self._write_excel(describe_excel_list=describe_excel_list,
                          attribute_manager=attribute_manager,
                          target_file=target_file)
        # 渲染excel
        self._render_target(describe_excel_list=describe_excel_list,
                            attribute_manager=attribute_manager,
                            target_file=target_file)

    def support(self, pay_type) -> bool:
        return True

    @PayLog(node="读取文件")
    def _read_file(self, file_dict: Dict[str, Iterable],
                   attribute_manager: AttributeManager) -> Dict[str, List[List[DataFrame]]]:
        return self._do_read_file(file_dict=file_dict,
                                  attribute_manager=attribute_manager)

    @abstractmethod
    def _do_read_file(self, file_dict: Dict[str, Iterable],
                      attribute_manager: AttributeManager) -> Dict[str, List[List[DataFrame]]]:
        pass

    @PayLog(node="解析数据")
    def _parse_df(self, df_dict: Dict[str, List[List[DataFrame]]],
                  attribute_manager: AttributeManager) -> List[DataFrame]:
        return self._do_parse_df(df_dict=df_dict,
                                 attribute_manager=attribute_manager)

    @abstractmethod
    def _do_parse_df(self, df_dict: Dict[str, List[List[DataFrame]]],
                     attribute_manager: AttributeManager) -> List[DataFrame]:
        pass

    @PayLog(node="索引重建")
    def _reset_index(self, df_list: List[DataFrame],
                     attribute_manager: AttributeManager):
        self._do_reset_index(df_list=df_list,
                             attribute_manager=attribute_manager)

    @abstractmethod
    def _do_reset_index(self, df_list: List[DataFrame],
                        attribute_manager: AttributeManager):
        pass

    @PayLog(node="创建excel描述")
    def _create_describe_4_excel(self, df_list: List[DataFrame],
                                 attribute_manager: AttributeManager) -> List[DescribeExcel]:
        return self._do_create_describe_4_excel(df_list=df_list,
                                                attribute_manager=attribute_manager)

    @abstractmethod
    def _do_create_describe_4_excel(self, df_list: List[DataFrame],
                                    attribute_manager: AttributeManager) -> List[DescribeExcel]:
        pass

    @PayLog(node="写入excel")
    def _write_excel(self, describe_excel_list: List[DescribeExcel],
                     attribute_manager: AttributeManager,
                     target_file: str):
        self._do_write_excel(describe_excel_list=describe_excel_list,
                             attribute_manager=attribute_manager,
                             target_file=target_file)

    @abstractmethod
    def _do_write_excel(self, describe_excel_list: List[DescribeExcel],
                        attribute_manager: AttributeManager,
                        target_file: str):
        pass

    @PayLog(node="渲染excel")
    def _render_target(self, describe_excel_list: List[DescribeExcel],
                       attribute_manager: AttributeManager,
                       target_file: str):
        self._do_render_target(describe_excel_list=describe_excel_list,
                               attribute_manager=attribute_manager,
                               target_file=target_file)

    @abstractmethod
    def _do_render_target(self, describe_excel_list: List[DescribeExcel],
                          attribute_manager: AttributeManager,
                          target_file: str):
        pass

    @PayLog(node="处理列")
    def _handle_column(self, df_list: List[DataFrame], attribute_manager: AttributeManager):
        self._do_handle_column(df_list=df_list, attribute_manager=attribute_manager)

    @abstractmethod
    def _do_handle_column(self, df_list: List[DataFrame], attribute_manager: AttributeManager):
        pass
