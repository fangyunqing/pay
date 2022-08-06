# @Time    : 22/07/22 11:27
# @Author  : fyq
# @File    : primary_frame.py
# @Software: PyCharm

__author__ = 'fyq'

import ttkbootstrap as ttk
from frame.bar_frame import BarFrame
from pay.pay_manager import PayManager
from frame.set_frame import SetFrame
from pathlib import Path
from frame.home_frame import HomeFrame


class PrimaryFrame(ttk.Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill=ttk.BOTH, expand=ttk.YES)
        self.pay_manager = PayManager()
        self.image_path = Path(__file__).parent.parent / 'assets'
        # 按钮信息
        self.buttons = [
            {
                "name": "home",
                "zh_name": "主页",
                "frame": HomeFrame(self, self.pay_manager),
                "image": ttk.PhotoImage(name="home", file=self.image_path / 'home.png')
            },
            {
                "name": "options",
                "zh_name": "设置",
                "frame": SetFrame(self, self.pay_manager),
                "image": ttk.PhotoImage(name="options", file=self.image_path / 'options.png')
            }
        ]

        BarFrame(master=self,
                 buttons=self.buttons,
                 action=self.action,
                 bootstyle=ttk.INFO
                 ).pack(side=ttk.LEFT, fill=ttk.Y)

    def action(self, frame_name):
        for button in self.buttons:
            if button["name"] == frame_name:
                button["frame"].pack(side=ttk.RIGHT, fill=ttk.BOTH, expand=ttk.YES)
            else:
                button["frame"].pack_forget()
