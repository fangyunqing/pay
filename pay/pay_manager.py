# @Time    : 22/06/22 9:12
# @Author  : fyq
# @File    : pay_manager.py
# @Software: PyCharm

__author__ = 'fyq'

import os
from pay.supplier.supplier_pay import SupplierPay
from pay.group.group_pay import GroupPay
import shutil
from util.model_util import ModelUtil
import time
import uuid


class PayManager:

    def __init__(self):
        self.calls = 3

    @staticmethod
    def _is_ignore_file(file):
        return file.startswith("~") or file in (".", "..") or not file.endswith((".xlsx", ".xls"))

    def parse(self, angle, model_name, path, template_file, callback, **kwargs):

        # 解析
        file_dict = {}
        callback("开始解析路径[%s]" % path)
        prefix_list = []
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                if self._is_ignore_file(file):
                    continue
                # 解析文件名 xx-xx-xx? 第二个xx为事业部名称
                val_list = os.path.splitext(file)[0].split("-")
                if len(val_list) > 1:
                    if val_list[1] not in file_dict:
                        file_dict[val_list[1]] = []
                    file_dict.get(val_list[1]).append(file_path)
                    prefix_list.append(val_list[0][:6])
            elif os.path.isdir(file_path) and file != "target":
                val_list = file.split("-")
                if len(val_list) == 1:
                    file_key = val_list[0]
                else:
                    file_key = val_list[1]
                for deep_file in os.listdir(file_path):
                    deep_file_path = os.path.join(file_path, deep_file)
                    if os.path.isfile(deep_file_path):
                        if self._is_ignore_file(deep_file):
                            continue
                        if file_key not in file_dict:
                            file_dict[file_key] = []
                        file_dict.get(file_key).append(deep_file_path)
        # 获取时间
        prefix_date = None
        for prefix in prefix_list:
            try:
                time.strptime(prefix, "%Y%m")
                prefix_date = prefix
            except ValueError:
                continue
        if prefix_date is None:
            raise Exception("从文件中没有发现可用的时间")
        # 创建文件夹
        target_dir = path + r"/target/"
        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)
        # 拷贝模板文件
        if "target" in kwargs:
            target_file = target_dir + prefix_date + kwargs["target"] + os.path.splitext(template_file)[1]
        else:
            target_file = path + r"/target/" + prefix_date + "target" + os.path.splitext(template_file)[1]
        callback("开始拷贝模板文件[%s]到[%s]" % (template_file, target_file))
        if os.path.isfile(target_file):
            uid = uuid.uuid1()
            tmp_file = target_file + "_" + str(uid)
            shutil.move(target_file, tmp_file)
        shutil.copy(template_file, target_file)
        # 分析文件
        callback("开始分析文件")
        attribute_data = ModelUtil(angle).read_file_only(model_name)
        for pay_name in attribute_data:
            if angle == "supplier":
                pay = SupplierPay(attribute_dict=attribute_data[pay_name])
            else:
                pay = GroupPay(attribute_dict=attribute_data[pay_name])
            pay.parse(file_dict, target_file)


