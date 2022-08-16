# @Time    : 22/08/09 14:44
# @Author  : fyq
# @File    : default_path_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import os
from loguru import logger
from pay.path_parser.path_parser import PathParser


class DefaultPathParser(PathParser):
    """
    默认路径解析器, 只会解析1级和2级路径
    """

    def parse_path(self, path, date_length):
        """
            1. 解析路径形成 file_dict
            2. 通过文件名获取到时间
        :param date_length: 时间长度
        :param path: 需要解析的路径
        :return:
        """
        logger.info("开始解析路径[%s]" % path)

        file_dict = {}
        prefix_list = []

        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                # 忽略部分文件
                if self._is_ignore_file(file):
                    continue
                # 解析文件名 xx-xx-xx 取第二个xx作为key
                val_list = os.path.splitext(file)[0].split("-")
                if len(val_list) > 1:
                    if val_list[1] not in file_dict:
                        file_dict[val_list[1]] = []
                    file_dict.get(val_list[1]).append(file_path)
                    if len(val_list[0]) >= date_length:
                        prefix_list.append(val_list[0][:date_length])
            elif os.path.isdir(file_path) and file != "target":
                val_list = file.split("-")
                if len(val_list) == 1:
                    file_key = val_list[0]
                else:
                    file_key = val_list[1]
                for deep_file in os.listdir(file_path):
                    deep_file_path = os.path.join(file_path, deep_file)
                    if os.path.isfile(deep_file_path):
                        # 忽略部分文件
                        if self._is_ignore_file(deep_file):
                            continue
                        if file_key not in file_dict:
                            file_dict[file_key] = []
                        file_dict.get(file_key).append(deep_file_path)
                        if len(val_list[0]) >= date_length:
                            prefix_list.append(val_list[0][:date_length])
        # 获取时间
        prefix_date = self._get_date(prefix_list)
        if prefix_date is None:
            logger.exception("从文件标题没有发现可用的时间")

        return prefix_date, file_dict


