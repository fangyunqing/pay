# @Time    : 23/02/01 13:23
# @Author  : fyq
# @File    : abstract_payable_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import abstractmethod
from typing import List, Optional, Dict, Iterable

from pandas import DataFrame

from pay.attribute import AttributeManager, common_attribute
from pay.create_describe_4_excel.describe_excel import DescribeExcel
from pay.decorator import PayLog
from pay.file_parser.file_parser import FileParser


class AbstractPayableFileParser(FileParser):

    def parse_file(self,
                   file_dict: Dict[str, Iterable],
                   target_file: Optional[str],
                   attribute_manager: AttributeManager) -> None:
        # 读取文件
        df_dict = self._read_file(file_dict=file_dict,
                                  attribute_manager=attribute_manager,
                                  ignore_not_exist=self._ignore_not_exist())
        # 解析文件
        df_list = self._parse_df(df_dict=df_dict,
                                 attribute_manager=attribute_manager)
        # 索引重建
        self._reset_index(df_list=df_list,
                          attribute_manager=attribute_manager)
        # 校对
        self._check(df_list=df_list,
                    attribute_manager=attribute_manager)
        # 创建excel描述符
        describe_excel_list = self._create_describe_4_excel(df_list=df_list,
                                                            attribute_manager=attribute_manager)
        # 写入excel
        self._write_excel(describe_excel_list=describe_excel_list,
                          attribute_manager=attribute_manager,
                          target_file=target_file)
        # 渲染excel
        common_attribute.first_column_merger_attr.value = self._first_column_merger()
        attribute_manager.add(common_attribute.first_column_merger_attr)
        self._render_target(describe_excel_list=describe_excel_list,
                            attribute_manager=attribute_manager,
                            target_file=target_file)

    @PayLog(node="读取文件")
    def _read_file(self, file_dict: Dict[str, Iterable],
                   attribute_manager: AttributeManager,
                   ignore_not_exist: bool) -> Dict[str, DataFrame]:
        return self._do_read_file(file_dict=file_dict,
                                  attribute_manager=attribute_manager,
                                  ignore_not_exist=ignore_not_exist)

    @abstractmethod
    def _do_read_file(self, file_dict: Dict[str, Iterable],
                      attribute_manager: AttributeManager,
                      ignore_not_exist: bool) -> Dict[str, DataFrame]:
        pass

    @PayLog(node="解析文件")
    def _parse_df(self, df_dict: Dict[str, DataFrame],
                  attribute_manager: AttributeManager) -> List[DataFrame]:
        return self._parse_df(df_dict=df_dict,
                              attribute_manager=attribute_manager)

    @abstractmethod
    def _do_parse_df(self, df_dict: Dict[str, DataFrame],
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

    @PayLog(node="校对")
    def _check(self, df_list: List[DataFrame],
               attribute_manager: AttributeManager):
        self._do_check(df_list=df_list,
                       attribute_manager=attribute_manager)

    @abstractmethod
    def _do_check(self, df_list: List[DataFrame],
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

    @abstractmethod
    def _ignore_not_exist(self) -> bool:
        pass

    @abstractmethod
    def _first_column_merger(self) -> int:
        pass
