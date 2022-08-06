# @Time    : 22/08/04 9:05
# @Author  : fyq
# @File    : home_choose_frame.py
# @Software: PyCharm

__author__ = 'fyq'

import ttkbootstrap as ttk
from util.model_util import ModelUtil
from tkinter import filedialog
from frame.label_edit_frame import LabelEditFrame


class HomeChooseFrame(ttk.Frame):

    def __init__(self, master, option_info, **kw):
        super().__init__(master, **kw)
        self.option_info = option_info
        self.target = self.option_info[1]
        # 单选框
        self.le_enable = LabelEditFrame(master=self,
                                        edit_type=LabelEditFrame.CHECK_BUTTON,
                                        label_text="生效")
        self.le_enable.pack(side=ttk.TOP, fill=ttk.X, padx=5, pady=5)
        # 文件夹选择
        self.le_dir = LabelEditFrame(master=self,
                                     label_text="文件夹",
                                     button_command="dir")
        self.le_dir.pack(side=ttk.TOP, fill=ttk.X, padx=5, pady=5)
        # 模板文件选择
        self.le_file = LabelEditFrame(master=self,
                                      label_text="模板文件",
                                      button_command="file")
        self.le_file.pack(side=ttk.TOP, fill=ttk.X, padx=5, pady=5)
        # 设置参数
        self.le_option = LabelEditFrame(master=self,
                                        edit_type=LabelEditFrame.COMBOBOX,
                                        label_text="设置参数",
                                        button_text="刷新",
                                        cb_values=ModelUtil(self.option_info[0]).model_list,
                                        button_command=self.option_refresh)
        self.le_option.pack(side=ttk.TOP, fill=ttk.X, padx=5, pady=5)

    def click_dir(self):
        open_dir = filedialog.askdirectory()
        if open_dir and len(open_dir) > 0:
            self.le_dir.value.set(open_dir)

    def click_model(self):
        open_model = filedialog.askopenfilename(
            filetypes=[('xlsx', '*.xlsx'), ('xls', '*.xls')])
        if open_model and len(open_model) > 0:
            self.le_file.value.set(open_model)

    def options(self):
        return self.option_info[0], {
            "val": self.le_enable.value.get(),
            "parse_dir": self.le_dir.value.get(),
            "model_file": self.le_file.value.get(),
            "target": self.target,
            "model_name": self.le_option.value.get()
        }

    def set_options(self, options):
        self.le_enable.value.set(options.get("val", 0))
        self.le_dir.value.set(options.get("parse_dir", "").replace("@@", ""))
        self.le_file.value.set(options.get("model_file", "").replace("@@", ""))
        self.target = options.get("target", self.option_info[1]).replace("@@", "")
        self.le_option.value.set(options.get("model_name", "").replace("@@", ""))

    def option_refresh(self):
        self.le_option.edit["values"] = ModelUtil(self.option_info[0]).model_list
