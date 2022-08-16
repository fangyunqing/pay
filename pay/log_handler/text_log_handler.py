# @Time    : 22/08/15 15:55
# @Author  : fyq
# @File    : text_log_handler.py
# @Software: PyCharm

__author__ = 'fyq'

import logging
import ttkbootstrap as ttk


class TextLogHandler(logging.Handler):

    def __init__(self, text):
        super().__init__()
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        self.text.insert(ttk.END, msg)
        self.text.insert(ttk.INSERT, '\n')
        self.text.see(ttk.END)
        self.text.update()
