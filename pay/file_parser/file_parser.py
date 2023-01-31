# @Time    : 22/08/12 14:42
# @Author  : fyq
# @File    : file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import ABCMeta, abstractmethod
from typing import Tuple, Optional, Dict, Iterable

from pay.attribute import AttributeManager


class FileParser(metaclass=ABCMeta):

    @abstractmethod
    def parse_file(self,
                   file_dict: Tuple[Optional[str], Dict[str, Iterable], Optional[str]],
                   target_file: Optional[str],
                   attribute_manager: AttributeManager) -> None:
        """
        :param file_dict: name:file-list
        :param target_file: 目标文件
        :param attribute_manager: 属性管理
        :return:
        """
        pass

    @abstractmethod
    def support(self, pay_type) -> bool:
        pass
