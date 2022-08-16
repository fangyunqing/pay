# @Time    : 22/08/12 13:37
# @Author  : fyq
# @File    : path_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import time
from abc import ABCMeta, abstractmethod


class PathParser(metaclass=ABCMeta):

    @classmethod
    def _is_ignore_file(cls, file):
        """
            是否是需要忽略的文件
                开头 ~ . ..
                结尾不为 xlsx xls
        :param file: 文件名
        :return:
        """
        return file.startswith("~") or file in (".", "..") or not file.endswith((".xlsx", ".xls"))

    @classmethod
    def _get_date(cls, prefix_list):
        for prefix in prefix_list:
            try:
                time.strptime(prefix, "%Y%m")
                return prefix
            except ValueError:
                continue

    @abstractmethod
    def parse_path(self, path, date_length):
        pass
