# @Time    : 22/09/28 8:52
# @Author  : fyq
# @File    : render.py
# @Software: PyCharm

__author__ = 'fyq'


from abc import ABCMeta, abstractmethod


class Render(metaclass=ABCMeta):

    @abstractmethod
    def render(self, describe_excel_list, attribute_manager, target_file):
        pass