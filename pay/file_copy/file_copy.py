# @Time    : 22/08/12 13:52
# @Author  : fyq
# @File    : file_copy.py
# @Software: PyCharm

__author__ = 'fyq'


from abc import ABCMeta, abstractmethod


class FileCopy(metaclass=ABCMeta):

    @abstractmethod
    def copy_file(self, template_file, prefix_date, path, target=None):
        raise NotImplementedError()
