# @Time    : 22/12/17 17:18
# @Author  : fyq
# @File    : diff_type_manager.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.decorator import singleton
from pay.file_parser.map.diff_type.diff_type_one import DiffTypeOne
from pay.file_parser.map.diff_type.diff_type_zero import DiffTypeZero


@singleton
class DiffTypeManager:

    def __init__(self):
        self.diff_type_list = [DiffTypeOne(), DiffTypeZero()]

    def get_diff_type(self, diff_type):
        for dt in self.diff_type_list:
            if dt.support() == diff_type:
                return dt
