# @Time    : 22/08/12 8:30
# @Author  : fyq
# @File    : attribute_checker.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import ABCMeta, abstractmethod

from pay.attribute_checker.common_checker import CommonChecker


class IAttributeChecker(metaclass=ABCMeta):

    def check_attribute(self, attribute_list):
        check_map = self.create_check_map()
        for attr in attribute_list:
            CommonChecker.check_strip_len(attr.text, attr.value, attr.required)
            if attr.name in check_map:
                check_map[attr.name](attr)

    @abstractmethod
    def create_check_map(self):
        pass
