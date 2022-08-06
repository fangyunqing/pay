# @Time    : 22/07/02 13:35
# @Author  : fyq
# @File    : model_util.py
# @Software: PyCharm

__author__ = 'fyq'

import os
import json


class ModelUtil:

    def __init__(self, model):
        self.model_dir = os.getcwd() + r"/" + model
        if not os.path.isdir(self.model_dir):
            os.mkdir(self.model_dir)

        self.model_list = []
        # 读取路径json结尾
        for file in os.listdir(self.model_dir):
            file_path = os.path.join(self.model_dir, file)
            if os.path.isfile(file_path) and file.endswith(".json"):
                self.model_list.append(os.path.splitext(file)[0])

    def read_file_only(self, model_name):
        model_name_path = os.path.join(self.model_dir, model_name) + ".json"
        with open(model_name_path, mode="r", encoding="utf-8") as f:
            f_data = json.load(f)
        for k1 in f_data.keys():
            for k2 in f_data[k1].keys():
                val = f_data[k1][k2]
                if isinstance(val, str):
                    f_data[k1][k2] = val.strip().replace('\n', '').replace('\r', '')
        return f_data

    def write_file(self, model_name, data, prefix=None):
        model_name_path = os.path.join(self.model_dir, model_name) + ".json"
        f_data = {}
        if prefix is None:
            prefix = ""
        for pay_name in data.keys():
            f_data_dict = {}
            f_data[pay_name] = f_data_dict
            for key, value in data[pay_name].items():
                if hasattr(value, "get"):
                    f_data_dict[key] = value.get()
                elif isinstance(value, str):
                    f_data_dict[key] = prefix + value + prefix
                else:
                    f_data_dict[key] = value

        with open(model_name_path, mode="wt", encoding="utf-8") as f:
            json.dump(f_data, f, ensure_ascii=False, indent=4)

        if model_name not in self.model_list:
            self.model_list.append(model_name)

    def read_file(self, model_name, data, prefix=None):
        model_name_path = os.path.join(self.model_dir, model_name) + ".json"
        try:
            with open(model_name_path, mode="r", encoding="utf-8") as f:
                f_data = json.load(f)
        except FileNotFoundError:
            return

        for pay_name in f_data.keys():
            if pay_name in data.keys():
                for key in f_data[pay_name].keys():
                    if key in data[pay_name].keys():
                        val = f_data[pay_name][key]
                        if isinstance(val, str):
                            val = val.strip().replace('\n', '').replace('\r', '')
                        if isinstance(val, str) and prefix is not None:
                            if val.startswith(prefix):
                                val = val[len(prefix):]
                            if val.endswith(prefix):
                                val = val[0:-len(prefix)]
                        if hasattr(data[pay_name][key], "set"):
                            data[pay_name][key].set(val)
                        else:
                            data[pay_name][key] = val
