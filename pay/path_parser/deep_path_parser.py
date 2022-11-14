# @Time    : 22/11/10 13:34
# @Author  : fyq
# @File    : deep_path_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import os

from pay.path_parser.path_parser import PathParser


class DeepPathParser(PathParser):

    """
        只读二级
    """

    def parse_path(self, path, date_length):

        file_dict = {}
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                if self._is_ignore_file(file):
                    continue
                file_name = os.path.splitext(file)[0]
                file_dict[file_name] = file_path
            elif os.path.isdir(file_path) and file != "target":
                file_dict[file] = []
                for deep_file in os.listdir(file_path):
                    deep_file_path = os.path.join(file_path, deep_file)
                    if os.path.isfile(deep_file_path):
                        if self._is_ignore_file(deep_file):
                            continue
                        file_dict[file].append(deep_file_path)

        return None, file_dict, None
