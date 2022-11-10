# @Time    : 22/11/09 10:27
# @Author  : fyq
# @File    : pdf_path_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import os
from pay.path_parser.path_parser import PathParser
from pay.decorator.pay_log import PayLog


class PdfPathParser(PathParser):

    @classmethod
    def _is_ignore_file(cls, file):
        return file.startswith("~") or file in (".", "..") or not file.endswith(".pdf")

    @PayLog(node="解析路径")
    def parse_path(self, path, date_length):
        file_dict = {}
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                if not self._is_ignore_file(file):
                    file = file.replace(".pdf", "")
                    file_dict[file] = [file_path]
        return None, file_dict, None




