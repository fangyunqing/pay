# @Time    : 23/01/31 15:08
# @Author  : fyq
# @File    : exceptions.py
# @Software: PyCharm

__author__ = 'fyq'


class PayException(Exception):
    def __init__(self, message=None):
        super().__init__(message)


class InvoicePayException(PayException):
    pass
