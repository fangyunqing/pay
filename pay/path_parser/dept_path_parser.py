# @Time    : 22/08/16 11:25
# @Author  : fyq
# @File    : dept_path_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import os
from pay.path_parser.path_parser import PathParser
from pay.decorator.pay_log import PayLog
from loguru import logger


class DeptPathParser(PathParser):

    @PayLog(node="解析路径")
    def parse_path(self, path, date_length):
        dept_name = os.path.basename(path)
        file_list = []
        file_dict = {dept_name: file_list}
        prefix_list = []
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path) and not self._is_ignore_file(file):
                file_list.append(file_path)
                if len(file) >= date_length:
                    prefix_list.append(file[:date_length])

        # 获取时间
        prefix_date = self._get_date(prefix_list)
        if prefix_date is None:
            logger.exception("从文件标题没有发现可用的时间")
        dept_name = dept_name.replace(prefix_date, "")
        return prefix_date, file_dict, dept_name
