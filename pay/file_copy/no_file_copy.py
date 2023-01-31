# @Time    : 22/08/26 15:40
# @Author  : fyq
# @File    : no_file_copy.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.file_copy.file_copy import FileCopy
from pay.decorator.pay_log import PayLog


class NoFileCopy(FileCopy):

    def copy_file(self, template_file, prefix_date, path, target=None):
        return template_file
