# @Time    : 22/06/22 9:12
# @Author  : fyq
# @File    : pay_manager.py
# @Software: PyCharm

__author__ = 'fyq'

from sortedcontainers import SortedKeyList
from util.model_util import ModelUtil
from pay import pay_type


class PayManager:

    def __init__(self):
        self.calls = 3
        self.pay_list = SortedKeyList(iterable=[pay_cls() for pay_cls in pay_type], key=lambda item: item.order())

    @staticmethod
    def _is_ignore_file(file):
        return file.startswith("~") or file in (".", "..") or not file.endswith((".xlsx", ".xls"))

    def parse(self, angle, model_name, path, template_file):
        attribute_data = ModelUtil(angle).read_file_only(model_name)
        for pay in self.pay_list:
            pay_info = pay.pay_name()
            if pay_info[0] == angle:
                pay.parse(attribute_data=attribute_data,
                          path=path,
                          template_file=template_file)

