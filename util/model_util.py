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
            return json.load(f)

    def write_file(self, model_name, data):
        model_name_path = os.path.join(self.model_dir, model_name) + ".json"
        f_data = {}
        for pay_name in data.keys():
            f_data[pay_name] = {key: value.get() if hasattr(value, "get") else value for key, value in data[pay_name].items()}

        with open(model_name_path, mode="wt", encoding="utf-8") as f:
            json.dump(f_data, f, ensure_ascii=False)

        if model_name not in self.model_list:
            self.model_list.append(model_name)

    def read_file(self, model_name, data):
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
                        if hasattr(data[pay_name][key], "set"):
                            data[pay_name][key].set(f_data[pay_name][key])
                        else:
                            data[pay_name][key] = f_data[pay_name][key]
