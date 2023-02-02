# @Time    : 23/01/31 14:53
# @Author  : fyq
# @File    : invoice_path_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import os
import re
from typing import Tuple, Dict, Optional, Iterable

from sortedcontainers import SortedKeyList

from pay import exceptions
from pay.path_parser.path_parser import PathParser
import datetime


class InvoicePathParser(PathParser):
    """
        路径格式
        第一级路径 any
            第二级路径 eg 0131 -> 2023-01-31
                第三级路径 excel文件 排序
    """

    replace_str_list = ("-", ".", "\\", "/")

    def parse_path(self, path, date_length) -> Tuple[Optional[str], Dict[str, Iterable], Optional[str]]:

        def sort(s: str) -> Optional[int]:
            pattern = re.compile(r"^(\d+)")
            ret = pattern.match(os.path.basename(s))
            if ret is None:
                return -1
            else:
                return int(ret.group(0))

        today = datetime.datetime.now()
        file_dict = {}
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path) and file != "target":
                file = file.strip()
                for replace_str in self.replace_str_list:
                    file = file.replace(replace_str, "")
                if len(file) == 3:
                    file = "0" + file
                if len(file) != 4:
                    raise exceptions.InvoicePayException(f"{file}不是一个正确的时间格式")
                invoice_time = str(today.year) + "-" + file[0:2] + "-" + file[2:4]
                file_dict[invoice_time] = SortedKeyList(key=sort)
                for deep_file in os.listdir(file_path):
                    if not self._is_ignore_file(deep_file):
                        file_dict[invoice_time].add(os.path.join(file_path, deep_file))
        return None, file_dict, None


