# @Time    : 23/02/25 13:09
# @Author  : fyq
# @File    : reconciliation_letter_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import datetime
import os
import pathlib
import shutil
from typing import Dict, Iterable, Any, List

import pandas as pd
import pythoncom
from loguru import logger
from xlwings import Sheet, App
from pay.attribute import AttributeManager
from pay.constant import attr_string
import pyparsing as pp

from pay.file_parser.reconciliation_letter.abstract_reconciliation_letter_file_parser import \
    AbstractReconciliationLetterFileParser


class ReconciliationLetterFileParser(AbstractReconciliationLetterFileParser):
    def _do_read_data(self, file_dict: Dict[str, Iterable],
                      attribute_manager: AttributeManager) -> Dict[str, pd.DataFrame]:
        datafile = attribute_manager.value(attr_string.datafile)
        skip_rows = attribute_manager.value(attr_string.skip_rows)
        if datafile not in file_dict:
            raise Exception(f"数据文件{datafile}未找到")
        data_df_dict = pd.read_excel(io=file_dict[datafile],
                                     skiprows=int(skip_rows),
                                     header=None,
                                     sheet_name=None)

        return data_df_dict

    def _do_read_map(self, file_dict: Dict[str, Any], attribute_manager: AttributeManager) -> pd.DataFrame:
        map_file = attribute_manager.value(attr_string.data_file)
        file_name, sheet_name, skip_rows = map_file.split(",")
        if file_name not in file_dict:
            raise Exception(f"对照文件{map_file}未找到")
        map_df = pd.read_excel(io=file_dict[file_name],
                               skiprows=int(skip_rows),
                               header=None,
                               sheet_name=sheet_name)
        return map_df

    def _do_gen(self, file_dict: Dict[str, Any], attribute_manager: AttributeManager,
                data_df_dict: Dict[str, pd.DataFrame], map_df: pd.DataFrame):
        model = "模板"
        if model not in file_dict:
            raise Exception(f"未找到模板文件夹")

        parse_path: str = file_dict["parse_path"]
        dir_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # 创建路径
        target_path = parse_path + os.path.sep + dir_name
        os.makedirs(target_path, exist_ok=True)
        model_dict: Dict[str, str] = {}
        for model_name in file_dict[model]:
            model_dict[os.path.splitext(os.path.basename(model_name))[0]] = model_name

        location_company: str = attribute_manager.value(attr_string.location_company)
        location_person: str = attribute_manager.value(attr_string.location_person)
        location_pay_currency: str = attribute_manager.value(attr_string.location_pay_currency)
        location_back_currency: str = attribute_manager.value(attr_string.location_back_currency)
        location_opening_currency: str = attribute_manager.value(attr_string.location_opening_currency)
        location_phone: str = attribute_manager.value(attr_string.location_phone)
        location_list: List[str] = [location_company, location_person, location_pay_currency,
                                    location_back_currency, location_opening_currency,
                                    location_phone]
        check_column = int(attribute_manager.value(attr_string.check_column))

        person_column = int(location_person.split(",")[0])
        pythoncom.CoInitialize()
        app = App(visible=False, add_book=False)
        try:
            app.display_alerts = False
            for data_name in data_df_dict.keys():

                map_rows = map_df[map_df[0] == data_name]
                model_paths: List[str] = []
                if len(map_rows) > 0:
                    os.makedirs(target_path + os.path.sep + data_name, exist_ok=True)
                    for map_index, map_rows in map_rows.iterrows():
                        mn: str = map_rows[1]
                        area: str = map_rows[2]
                        if mn in model_dict:
                            model_path = model_dict[mn]
                            model_paths.append(mn + "," +
                                               os.path.splitext(model_path)[1] + "," +
                                               model_path + "," +
                                               area)
                        else:
                            logger.warning(f"工作簿{data_name}未找到对应模板")
                else:
                    logger.warning(f"工作簿{data_name}未找到对应模板")

                if len(model_paths) == 0:
                    continue

                data_df = data_df_dict[data_name]
                data_df = data_df[data_df[check_column] == "是"]

                persons = data_df[person_column].unique().tolist()
                for p in persons:
                    p_df = data_df[data_df[person_column] == p]

                    if len(p_df) == 0:
                        continue

                    for model_path in model_paths:
                        mn, ext, mp, area = model_path.split(",")
                        target_file_path = target_path + os.path.sep + data_name + os.path.sep + mn + "-" + p + ext
                        des_wb = app.books.add()
                        try:
                            for data_index, data_row in p_df.iterrows():
                                # 打开源头excel
                                src_wb = app.books.open(mp)
                                try:
                                    sheet = src_wb.sheets[0]
                                    for location in location_list:
                                        loc, row, col, text = location.split(",")
                                        val = data_row[int(loc)]
                                        row = int(row) + 1
                                        col = int(col) + 1
                                        old_val: str = sheet.range((row, col)).value
                                        if text and len(text) > 0:
                                            if text in old_val:
                                                new_val = old_val.replace(text, str(val))
                                            else:
                                                new_val = val
                                        else:
                                            new_val = val

                                        sheet.range((row, col)).value = new_val
                                    # 复制工作簿
                                    sheet.copy(after=des_wb.sheets[0])
                                finally:
                                    src_wb.close()
                            des_wb.sheets[0].delete()
                            for des_sheet in des_wb.sheets:
                                des_sheet.api.PageSetup.PaperSize = 8
                                des_sheet.api.PageSetup.Orientation = 2
                                des_sheet.api.PageSetup.PrintArea = area
                        finally:
                            des_wb.save(target_file_path)
                            des_wb.close()
        finally:
            app.quit()
            app.kill()
            pythoncom.CoUninitialize()
