# @Time    : 23/01/31 16:50
# @Author  : fyq
# @File    : abstract_invoice_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import abstractmethod
from typing import Tuple, Optional, Dict, Iterable

from pay.attribute import AttributeManager
from pay.decorator import PayLog
from pay.file_parser.file_parser import FileParser


class AbstractInvoiceFileParser(FileParser):

    def parse_file(self, file_dict: Tuple[Optional[str], Dict[str, Iterable], Optional[str]],
                   target_file: Optional[str], attribute_manager: AttributeManager) -> None:
        pass

    def support(self, pay_type) -> bool:
        return True

    @PayLog(node="解析数据")
    def _parse_data(self, file_dict: Tuple[Optional[str], Dict[str, Iterable], Optional[str]],
                    attribute_manager: AttributeManager):
        self._do_parse_data(file_dict=file_dict,
                            attribute_manager=attribute_manager)

    @abstractmethod
    def _do_parse_data(self, file_dict: Tuple[Optional[str], Dict[str, Iterable], Optional[str]],
                       attribute_manager: AttributeManager):
        pass
