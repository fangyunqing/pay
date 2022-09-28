# @Time    : 22/08/26 15:31
# @Author  : fyq
# @File    : simple_path_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import os
from loguru import logger
from pay.path_parser.path_parser import PathParser
from pay.decorator.pay_log import PayLog


class SimplePathParser(PathParser):

    @PayLog(node="解析路径")
    def parse_path(self, path, date_length):
        file_dict = {}
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                if not self._is_ignore_file(file):
                    file = file.replace(".xlsx", "").replace(".xls", "").strip()
                    file_dict[file] = [file_path]
        return None, file_dict, None
