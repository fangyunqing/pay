# @Time    : 22/07/22 13:44
# @Author  : fyq
# @File    : set_frame.py
# @Software: PyCharm

__author__ = 'fyq'

import ttkbootstrap as ttk
from util.model_util import ModelUtil
from frame.label_edit_frame import LabelEditFrame
from ttkbootstrap.scrolled import ScrolledFrame


class SetFrame(ttk.Frame):

    def __init__(self, master, pay_manager, **kwargs):
        super().__init__(master, **kwargs)
        self.pay_manager = pay_manager

        top_fr = ttk.Frame(self)
        top_fr.pack(side=ttk.TOP, fill=ttk.BOTH, expand=ttk.YES)
        self.notebook = ttk.Notebook(top_fr)
        self.notebook.pack(side=ttk.RIGHT, fill=ttk.BOTH, expand=ttk.YES, padx=5, pady=5)
        bottom_fr = ttk.Frame(self)
        bottom_fr.pack(side=ttk.BOTTOM, fill=ttk.X)
        # pay
        self.str_pay = ttk.StringVar(value="")
        self.cb_pay = ttk.Combobox(master=bottom_fr, state="readonly", textvariable=self.str_pay,
                                   values=[pay.pay_name()[1] for pay in self.pay_manager.pay_list])
        self.cb_pay.pack(side=ttk.LEFT, padx=5, pady=5)
        self.cb_pay.bind("<<ComboboxSelected>>", self.pay_select)
        # model
        self.str_model = ttk.StringVar(value="")
        self.cb_model = ttk.Combobox(master=bottom_fr, textvariable=self.str_model)
        self.cb_model.pack(side=ttk.LEFT, padx=5, pady=5)
        self.cb_model.bind("<<ComboboxSelected>>", self.model_select)
        # save
        ttk.Button(bottom_fr, text="保存", command=self.model_save) \
            .pack(side=ttk.LEFT, anchor=ttk.CENTER, padx=5, pady=5)
        # model util
        self.mu = None
        # option data
        self.option_data = {}

    def pay_select(self, event):
        f_pay_list = list(filter(lambda pay: pay.pay_name()[1] == self.str_pay.get(),
                                 self.pay_manager.pay_list))
        if len(f_pay_list) > 0:
            f_pay = f_pay_list[0]
            self.mu = ModelUtil(f_pay.pay_name()[0])
            if len(self.mu.model_list) > 0:
                self.cb_model["values"] = self.mu.model_list
                self.cb_model.set("")
            else:
                self.cb_model["values"] = []
                self.cb_model.set("")

            for tab in self.notebook.tabs():
                self.notebook.forget(tab)
                self.option_data.clear()
            for pay_option in f_pay.pay_options():
                tab_fr = ScrolledFrame(self.notebook)
                self.notebook.add(tab_fr.container, text=pay_option[1])
                option_value = {}
                self.option_data[pay_option[1]] = option_value
                for attribute in f_pay.attribute_list(pay_option[1]).attribute_list:
                    cf = LabelEditFrame(master=tab_fr,
                                        label_text=attribute.text,
                                        button_command="detail",
                                        entry_type=attribute.data_type,
                                        label_width=12,
                                        label_wrap_length=80)
                    cf.pack(side=ttk.TOP, fill=ttk.X, padx=10, pady=10)
                    option_value[attribute.name] = cf.value

    def model_select(self, event):
        self.mu.read_file(self.str_model.get(), self.option_data)

    def model_save(self):
        model_name = self.str_model.get()
        if model_name is not None and len(model_name) > 0:
            self.mu.write_file(model_name, self.option_data)
            self.cb_model["values"] = self.mu.model_list
