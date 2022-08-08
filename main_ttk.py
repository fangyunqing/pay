# @Time    : 22/08/05 14:03
# @Author  : fyq
# @File    : main_ttk.py
# @Software: PyCharm

__author__ = 'fyq'

import ttkbootstrap as ttk
from frame.primary_frame import PrimaryFrame
import traceback
from ttkbootstrap.dialogs.dialogs import Messagebox


def print_exception(exc, val, tb):
    traceback.print_exception(exc, val, tb)
    err_msg = repr(exc) + "\n" + traceback.format_exc()
    Messagebox.show_error(message=err_msg, title="错误")


def thread_error(event):
    pass


app = ttk.Window("Pay", "yeti")
PrimaryFrame(app)
app.geometry("750x600")
app.position_center()
app.iconbitmap(default='assets/small.ico')
app.report_callback_exception = print_exception
app.bind("<<Thread_ERROR>>", thread_error)
app.mainloop()
