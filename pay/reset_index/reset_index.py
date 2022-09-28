# @Time    : 22/09/27 9:08
# @Author  : fyq
# @File    : reset_index.py
# @Software: PyCharm

__author__ = 'fyq'


from abc import ABCMeta, abstractmethod


class ResetIndex(metaclass=ABCMeta):

    @abstractmethod
    def reset_index(self, df_list, attribute_manager):
        pass
