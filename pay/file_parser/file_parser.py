# @Time    : 22/08/12 14:42
# @Author  : fyq
# @File    : file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import ABCMeta, abstractmethod


class FileParser(metaclass=ABCMeta):

    @abstractmethod
    def parse_file(self,
                   file_dict,
                   target_file,
                   attribute_manager):
        """
        :param file_dict: name:file-list
        :param target_file: 目标文件
        :param attribute_manager: 属性管理
        :return:
        """
        pass
