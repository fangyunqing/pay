# @Time    : 2023/07/01 10:34
# @Author  : fyq
# @File    : abstract_freeze_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import abstractmethod
from typing import Dict, Optional, Any

from pay.attribute import AttributeManager
from pay.decorator import PayLog
from pay.file_parser.file_parser import FileParser


class AbstractFreezeFileParser(FileParser):

    def parse_file(self, file_dict: Dict[str, Any], target_file: Optional[str],
                   attribute_manager: AttributeManager) -> None:
        self._freeze(file_dict=file_dict,
                     attribute_manager=attribute_manager)

    @PayLog(node="冻结开始")
    def _freeze(self, file_dict: Dict[str, Any], attribute_manager: AttributeManager):
        self._do_freeze(file_dict, attribute_manager)

    @abstractmethod
    def _do_freeze(self, file_dict: Dict[str, Any], attribute_manager: AttributeManager):
        pass

    def support(self, pay_type) -> bool:
        return True
