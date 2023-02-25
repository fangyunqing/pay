# @Time    : 23/02/25 12:53
# @Author  : fyq
# @File    : abstract_reconciliation_letter_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import abstractmethod
from typing import Dict, Iterable, Optional

from pay.attribute import AttributeManager
from pay.decorator import PayLog
from pay.file_parser.file_parser import FileParser
import pandas as pd


class AbstractReconciliationLetterFileParser(FileParser):

    def parse_file(self, file_dict: Dict[str, Iterable], target_file: Optional[str],
                   attribute_manager: AttributeManager) -> None:
        data_df_dict = self._read_data(file_dict=file_dict,
                                       attribute_manager=attribute_manager)

        map_df = self._read_map(file_dict=file_dict,
                                attribute_manager=attribute_manager)

        self._gen(file_dict=file_dict,
                  attribute_manager=attribute_manager,
                  data_df_dict=data_df_dict,
                  map_df=map_df)

    @PayLog(node="读取数据文件")
    def _read_data(self, file_dict: Dict[str, Iterable],
                   attribute_manager: AttributeManager) -> Dict[str, pd.DataFrame]:
        return self._do_read_data(file_dict=file_dict, attribute_manager=attribute_manager)

    @abstractmethod
    def _do_read_data(self, file_dict: Dict[str, Iterable],
                      attribute_manager: AttributeManager) -> Dict[str, pd.DataFrame]:
        pass

    @PayLog(node="读取对照文件")
    def _read_map(self, file_dict: Dict[str, Iterable],
                  attribute_manager: AttributeManager) -> pd.DataFrame:
        return self._do_read_map(file_dict=file_dict, attribute_manager=attribute_manager)

    @abstractmethod
    def _do_read_map(self, file_dict: Dict[str, Iterable],
                     attribute_manager: AttributeManager) -> pd.DataFrame:
        pass

    @PayLog(node="生成账单函")
    def _gen(self,
             file_dict: Dict[str, Iterable],
             attribute_manager: AttributeManager,
             data_df_dict: Dict[str, pd.DataFrame],
             map_df: pd.DataFrame):
        self._do_gen(file_dict=file_dict,
                     attribute_manager=attribute_manager,
                     data_df_dict=data_df_dict,
                     map_df=map_df)

    @abstractmethod
    def _do_gen(self,
                file_dict: Dict[str, Iterable],
                attribute_manager: AttributeManager,
                data_df_dict: Dict[str, pd.DataFrame],
                map_df: pd.DataFrame):
        pass

    def support(self, pay_type) -> bool:
        return True
