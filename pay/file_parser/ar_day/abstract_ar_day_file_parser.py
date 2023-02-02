# @Time    : 23/02/01 15:04
# @Author  : fyq
# @File    : abstract_ar_day_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import abstractmethod
from typing import Dict, Iterable, Optional, List

from pandas import DataFrame

from pay.attribute import AttributeManager
from pay.create_describe_4_excel.describe_excel import DescribeExcel
from pay.decorator import PayLog
from pay.file_parser.file_parser import FileParser


class AbstractARDayFileParser(FileParser):

    def parse_file(self, file_dict: Dict[str, Iterable], target_file: Optional[str],
                   attribute_manager: AttributeManager) -> None:
        # 客户对照表
        client_map_df = self._read_client_map_data(file_dict=file_dict,
                                                   attribute_manager=attribute_manager)
        # 应收出纳表
        ar_day_df = self._read_ar_day_data(file_dict=file_dict,
                                           attribute_manager=attribute_manager)
        # 合并数据
        df_list = self._merger(client_map_df=client_map_df,
                               ar_day_df=ar_day_df,
                               attribute_manager=attribute_manager)
        # excel描述符
        describe_excel_list = self._create_describe_4_excel(df_list=df_list,
                                                            attribute_manager=attribute_manager)
        # 渲染excel
        self._render_target(describe_excel_list=describe_excel_list,
                            attribute_manager=attribute_manager,
                            target_file=target_file)

    def support(self, pay_type) -> bool:
        return True

    @PayLog(node="读取用户对照表")
    def _read_client_map_data(self, file_dict: Dict[str, Iterable], attribute_manager: AttributeManager) -> DataFrame:
        return self._do_read_client_map_data(file_dict=file_dict,
                                             attribute_manager=attribute_manager)

    @abstractmethod
    def _do_read_client_map_data(self, file_dict: Dict[str, Iterable],
                                 attribute_manager: AttributeManager) -> DataFrame:
        pass

    @PayLog(node="读取应收收纳表")
    def _read_ar_day_data(self, file_dict: Dict[str, Iterable], attribute_manager: AttributeManager) -> DataFrame:
        return self._do_read_ar_day_data(file_dict=file_dict,
                                         attribute_manager=attribute_manager)

    @abstractmethod
    def _do_read_ar_day_data(self, file_dict: Dict[str, Iterable], attribute_manager: AttributeManager) -> DataFrame:
        pass

    @PayLog(node="合并数据")
    def _merger(self, client_map_df: DataFrame, ar_day_df: DataFrame,
                attribute_manager: AttributeManager) -> List[DataFrame]:
        return self._merger(client_map_df=client_map_df,
                            ar_day_df=ar_day_df,
                            attribute_manager=attribute_manager)

    @abstractmethod
    def _do_merger(self, client_map_df: DataFrame, ar_day_df: DataFrame,
                   attribute_manager: AttributeManager) -> List[DataFrame]:
        pass

    @PayLog(node="创建excel文件描述")
    def _create_describe_4_excel(self, df_list: List[DataFrame], attribute_manager: AttributeManager):
        return self._do_create_describe_4_excel(df_list, attribute_manager)

    @abstractmethod
    def _do_create_describe_4_excel(self, df_list: List[DataFrame], attribute_manager: AttributeManager):
        pass

    @PayLog(node="渲染excel")
    def _render_target(self, describe_excel_list: List[DescribeExcel],
                       attribute_manager: AttributeManager,
                       target_file: str):
        self._do_render_target(describe_excel_list, attribute_manager, target_file)

    @abstractmethod
    def _do_render_target(self, describe_excel_list: List[DescribeExcel],
                          attribute_manager: AttributeManager,
                          target_file: str):
        pass
