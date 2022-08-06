# @Time    : 22/07/22 15:26
# @Author  : fyq
# @File    : label_edit_frame.py
# @Software: PyCharm

__author__ = 'fyq'

import ttkbootstrap as ttk
from tkinter import filedialog


class LabelEditFrame(ttk.Frame):

    ENTRY = "entry"
    CHECK_BUTTON = "check_button"
    COMBOBOX = "combobox"

    def __init__(self, master, **kwargs):

        """
        :param master:
        :param kwargs:
            edit_type:
                ENTRY,CHECK_BUTTON
                默认 ENTRY
            label_text:
                默认空
            label_width:
                默认10
            label_anchor:
                ttk.E N S ..
                默认ttk.E
            label_wrap_length:
                默认100
            button_command:
                function or str
                str eg: "dir" "file" "detail" None
                默认 none
            button_text:
                默认 详情
            cb_values:
                默认 []
            entry_type:
                "int", "str"
                默认 str
        """

        # 类型
        self.edit_type = kwargs.pop("edit_type", self.ENTRY)
        # 标签的文本
        self.label_text = kwargs.pop("label_text", "")
        # 标签的长度
        self.label_width = kwargs.pop("label_width", 10)
        # 标签文本的位置
        self.label_anchor = kwargs.pop("label_anchor", ttk.E)
        # 标签多行的情况多长换行
        self.label_wrap_length = kwargs.pop("label_wrap_length", 120)
        # 按钮的点击事件
        self.button_command = kwargs.pop("button_command", None)
        # 按钮的文本
        self.button_text = kwargs.pop("button_text", "详情")
        # 组合框下拉值
        self.cb_values = kwargs.pop("cb_values", [])
        # 文本框的类型
        self.entry_type = kwargs.pop("entry_type", "str")
        # 基类
        super().__init__(master, **kwargs)
        # 保存的值
        if self.edit_type in [self.ENTRY, self.COMBOBOX]:
            if self.edit_type == self.ENTRY:
                if self.entry_type == "int":
                    self.value = ttk.IntVar()
                else:
                    self.value = ttk.StringVar(value="")
            else:
                self.value = ttk.StringVar(value="")
        elif self.edit_type in [self.CHECK_BUTTON]:
            self.value = ttk.IntVar()
        else:
            self.value = ttk.StringVar(value="")
        # 标签
        ttk.Label(
            master=self,
            text=self.label_text,
            width=self.label_width,
            anchor=self.label_anchor,
            wraplength=self.label_wrap_length).pack(side=ttk.LEFT, padx=5, pady=5)
        # 编辑框
        if self.edit_type == self.ENTRY:
            self.edit = ttk.Entry(master=self, textvariable=self.value)
        elif self.edit_type == self.CHECK_BUTTON:
            self.edit = ttk.Checkbutton(master=self, variable=self.value, onvalue=1, offvalue=0)
        elif self.edit_type == self.COMBOBOX:
            self.edit = ttk.Combobox(master=self,
                                     textvariable=self.value,
                                     values=self.cb_values)
        else:
            self.edit = ttk.Entry(master=self, textvariable=self.value)
        self.edit.pack(side=ttk.LEFT, fill=ttk.X, expand=ttk.YES, padx=5, pady=5)
        # 按钮
        if self.button_command:
            self.bt_detail = ttk.Button(
                master=self,
                text=self.button_text,
                width=5,
                command=self._bt_detail_click)
            self.bt_detail.pack(side=ttk.RIGHT, padx=5, pady=5)
        # 详情窗口
        self.detail_fr = None
        self.tx_detail = None

    def _bt_detail_click(self):
        if callable(self.button_command):
            self.button_command()
        elif self.button_command == "detail":
            self.command_detail()
        elif self.button_command == "file":
            self.command_file()
        elif self.button_command == "dir":
            self.command_dir()

    def delete_detail_fr(self):
        self.detail_fr.destroy()
        self.detail_fr = None

    def detail_save(self):
        self.value.set(self.tx_detail.get("1.0", ttk.END))
        self.delete_detail_fr()

    def command_detail(self):
        from frame.detail_messagebox import DetailMessageBox
        box = DetailMessageBox(title="文件", value=self.value.get())
        box.show()
        if box.result:
            self.value.set(box.result)

    def command_file(self):
        open_file = filedialog.askopenfilename(
            filetypes=[('xlsx', '*.xlsx'), ('xls', '*.xls')])
        if open_file and len(open_file) > 0:
            self.value.set(open_file)

    def command_dir(self):
        open_dir = filedialog.askdirectory()
        if open_dir and len(open_dir) > 0:
            self.value.set(open_dir)
