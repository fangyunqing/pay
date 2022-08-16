# @Time    : 22/08/12 8:30
# @Author  : fyq
# @File    : attribute_checker.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import ABCMeta, abstractmethod


class IAttributeChecker(metaclass=ABCMeta):

    @abstractmethod
    def check_attribute(self, attribute_list):
        pass
