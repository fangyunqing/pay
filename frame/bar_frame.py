# @Time    : 22/07/22 10:57
# @Author  : fyq
# @File    : bar_frame.py
# @Software: PyCharm

__author__ = 'fyq'

import ttkbootstrap as ttk
from functools import partial


class BarFrame(ttk.Frame):

    def __init__(self, master, buttons, action, **kwargs):
        super().__init__(master, **kwargs)
        self.images = [button["image"] for button in buttons]
        for button in buttons:
            ttk.Button(
                master=self,
                image=button["name"],
                text=button["zh_name"],
                compound=ttk.TOP,
                bootstyle=kwargs.get("bootstyle", ttk.INFO),
                command=partial(action, button["name"])
            ).pack(side=ttk.TOP, fill=ttk.BOTH, ipadx=10, ipady=10)
