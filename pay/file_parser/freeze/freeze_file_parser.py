# @Time    : 2023/07/01 10:47
# @Author  : fyq
# @File    : freeze_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import datetime
import os
from typing import Dict, Any

import pythoncom
from loguru import logger
from xlwings import App

from pay.attribute import AttributeManager
from pay.constant import attr_string
from pay.file_parser.freeze.abstract_freeze_file_parser import AbstractFreezeFileParser

import shutil


class FreezeFileParser(AbstractFreezeFileParser):

    def _do_freeze(self, file_dict: Dict[str, Any], attribute_manager: AttributeManager):
        # 拷贝文件
        parse_path: str = file_dict.pop("parse_path")
        dir_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        target_path = f"{parse_path}{os.sep}target{os.sep}{dir_name}"
        os.makedirs(target_path)
        # 解析冻结规则
        rules: str = attribute_manager.value(attr_string.info)
        rule_list = []
        for rule in rules.splitlines():
            if len(rule) > 0:
                sub_rule_list = rule.split()[0:2]
                if len(sub_rule_list) == 2:
                    rule_list.append(sub_rule_list)
                else:
                    logger.warning(f"[{rule}]不符合规范")
        # 开始冻结
        pythoncom.CoInitialize()
        app = App(visible=False, add_book=False)
        try:
            app.display_alerts = False
            for _, file_path in file_dict.items():
                target_file_path = shutil.copy(file_path, target_path)
                wb = app.books.open(target_file_path)
                try:
                    for sheet_name, c_r in rule_list:
                        sheet_name = sheet_name.strip()
                        sheet_names = [st.name for st in wb.sheets]
                        if sheet_name in sheet_names:
                            sheet = wb.sheets[sheet_name]
                        elif sheet_name + " " in sheet_names:
                            sheet = wb.sheets[sheet_name + " "]
                        elif " " + sheet_name in sheet_names:
                            sheet = wb.sheets[" " + sheet_name]
                        elif " " + sheet_name + " " in sheet_names:
                            sheet = wb.sheets[" " + sheet_name + " "]
                        else:
                            logger.warning(f"[{file_path}]未找到[{sheet_name}]")
                            continue
                        sheet.select()
                        sheet.range(c_r).select()
                        app.api.ActiveWindow.FreezePanes = True
                    if len(wb.sheets) > 0:
                        wb.sheets[0].select()
                finally:
                    wb.save()
                    wb.close()
        finally:
            app.quit()
            app.kill()
            pythoncom.CoUninitialize()
