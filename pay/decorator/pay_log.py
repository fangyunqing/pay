# @Time    : 22/08/16 10:24
# @Author  : fyq
# @File    : pay_log.py
# @Software: PyCharm

__author__ = 'fyq'

import functools
import time

from loguru import logger


class PayLog:

    def __init__(self, node):
        self.node = node

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info("开始%s" % self.node)
            begin_time = time.perf_counter()
            result = func(*args, **kwargs)
            logger.info("结束{},用时{:.5f}秒".format(self.node, time.perf_counter() - begin_time))
            return result
        return wrapper
