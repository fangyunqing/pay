# @Time    : 22/08/03 16:11
# @Author  : fyq
# @File    : home_frame.py
# @Software: PyCharm

__author__ = 'fyq'

import threading
import time

import ttkbootstrap as ttk
from frame.home_choose_frame import HomeChooseFrame
from util.model_util import ModelUtil
import traceback
from ttkbootstrap.dialogs.dialogs import Messagebox


class HomeFrame(ttk.Frame):

    def __init__(self, master, pay_manager, **kwargs):
        super().__init__(master, **kwargs)
        self.pay_manager = pay_manager
        self.option_fr_list = []
        # 标题头
        title_fr = ttk.Frame(self)
        title_fr.pack(side=ttk.TOP, fill=ttk.X)
        ttk.Button(master=title_fr,
                   text="保存选择项",
                   command=self.store_option).pack(side=ttk.LEFT, padx=5, pady=5)
        ttk.Button(master=title_fr,
                   text="还原选择项",
                   command=self.restore_option).pack(side=ttk.LEFT, padx=5, pady=5)
        ttk.Button(master=title_fr,
                   text="开始",
                   command=self.start).pack(side=ttk.LEFT, padx=5, pady=5)
        self.pb_parse = ttk.Progressbar(
            master=title_fr,
            maximum=100,
            bootstyle=(ttk.SUCCESS, ttk.STRIPED))
        self.pb_parse.pack(side=ttk.LEFT, fill=ttk.X, expand=ttk.YES, padx=5, pady=5)
        self.pb_parse["value"] = 0

        # 选择项
        choose_fr = ttk.Frame(self)
        choose_fr.pack(side=ttk.TOP, fill=ttk.X)
        self.nb_option = ttk.Notebook(master=choose_fr)
        self.nb_option.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=ttk.YES, padx=5, pady=5)
        for pay in self.pay_manager.pay_list:
            tab_fr = HomeChooseFrame(master=self.nb_option, option_info=pay.pay_name())
            self.nb_option.add(tab_fr, text=pay.pay_name()[1])
            self.option_fr_list.append(tab_fr)

        # 信息提示项
        message_fr = ttk.Frame(self)
        message_fr.pack(side=ttk.TOP, fill=ttk.BOTH, expand=ttk.YES)
        self.tx_msg = ttk.Text(master=message_fr)
        self.tx_msg.pack(side=ttk.TOP, fill=ttk.BOTH, expand=ttk.YES, padx=5, pady=5)

    def store_option(self):
        option_dict = {}
        for tab in self.option_fr_list:
            option, options = tab.options()
            option_dict[option] = options
        ModelUtil("pay_tool").write_file("default", option_dict)

    def restore_option(self):
        option_dict = ModelUtil("pay_tool").read_file_only("default")
        for tab in self.option_fr_list:
            option = tab.options()[0]
            if option in option_dict.keys():
                tab.set_options(option_dict[option])

    def start(self):
        option_dict = {}
        for tab in self.option_fr_list:
            option, options = tab.options()
            if options.get("val") == 1 and len(options.get("parse_dir")) > 0 and len(
                    options.get("model_file")) > 0 and len(options.get("model_name")) > 0:
                option_dict[option] = options
        if len(option_dict.keys()) > 0:
            t = threading.Thread(target=self.thread_func, args=(option_dict,))
            t.setDaemon(True)
            t.start()

    def print_msg(self, msg):
        self.tx_msg.insert(ttk.END, msg)
        self.tx_msg.insert(ttk.INSERT, '\n')
        self.tx_msg.see(ttk.END)
        self.tx_msg.update()

    def callback(self, msg):
        self.pb_parse["value"] = self.pb_parse["value"] + 1
        self.print_msg(msg)

    def thread_func(self, option_dict):

        try:
            self.pb_parse['maximum'] = len(option_dict.keys()) * self.pay_manager.calls
            self.pb_parse["value"] = 0
            self.tx_msg.delete(1.0, ttk.END)
            self.winfo_toplevel().attributes("-disabled", True)
            begin_time = time.time()
            for key in option_dict.keys():
                options = option_dict[key]
                self.pay_manager.parse(angle=key,
                                       model_name=options.get("model_name"),
                                       path=options.get("parse_dir"),
                                       template_file=options.get("model_file"),
                                       callback=self.callback,
                                       target=options.get("target"))
            self.print_msg("总共用时：{:.2f}秒".format(time.time() - begin_time))
        except Exception as e:
            traceback.print_exc()
            err_msg = repr(e) + "\n" + traceback.format_exc()
            self.winfo_toplevel().after(100, func=lambda: Messagebox.show_error(err_msg))
        finally:
            self.pb_parse["value"] = 0
            self.winfo_toplevel().attributes("-disabled", False)
