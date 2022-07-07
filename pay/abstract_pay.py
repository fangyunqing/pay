# @Time    : 22/06/22 8:40
# @Author  : fyq
# @File    : abstract_pay.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import ABCMeta, abstractmethod
import numpy as np
import pandas as pd
import xlwings as xl
import os
import calendar
import pythoncom


class AbstractPay(metaclass=ABCMeta):

    def __init__(self, attribute_dict):
        self.attribute_dict = attribute_dict
        self.dept_column = "dept"

    def __getitem__(self, item):
        try:
            return self.attribute_dict[item]
        except KeyError:
            return None

    @staticmethod
    def get_supplier_useless_field():
        return ["小计", "合计", "", np.nan]

    @abstractmethod
    def _parse(self, df_list):
        pass

    def _write_excel(self, target_file, df_list):
        with pd.ExcelWriter(target_file, engine='openpyxl', mode='a', if_sheet_exists="overlay") as writer:
            sheet_name, start_row = self["write_sheet"].split(",")
            df_list[0].to_excel(writer,
                                startrow=int(start_row),
                                sheet_name=sheet_name,
                                header=None,
                                index=None)

        return [(len(df_list[0].index), len(df_list[0].columns), int(start_row), target_file, sheet_name)]

    def parse(self, file_dict, target_file):
        pd.set_option('display.max_columns', None)
        df_list = []
        for key in file_dict:
            dept_file = []
            for file in file_dict[key]:
                df = pd.read_excel(file, sheet_name=self["read_sheet"], skiprows=self["skip_rows"], header=None)
                useless_column = []
                for value in df.columns:
                    if str(value) not in self["use_column"]:
                        useless_column.append(value)
                # 去除供应商无用的行
                df.drop(df[df[self["supplier_column"]].isin(self.get_supplier_useless_field())].index,
                        inplace=True)
                # 添加编制单位列
                df.insert(column=self.dept_column, value=key, loc=0)
                # 去除无用的列
                if len(useless_column) > 0:
                    df.drop(useless_column, axis=1, inplace=True, errors="ignore")
                # 处理类型空值
                df[self["type_column"]].fillna("未知分类", inplace=True)
                # 加入到队列中
                dept_file.append(df)
            if len(dept_file) > 0:
                df_list.append(pd.concat(dept_file))

        df_parse_list = self._parse(df_list)
        write_info = self._write_excel(target_file, df_parse_list)
        for df_row, df_column, start_row, target_file, sheet_name in write_info:
            self._set_style(df_row, df_column, start_row, target_file, sheet_name)

    def _set_style(self, df_len, df_column, start_row, target_file, sheet_name):
        pythoncom.CoInitialize()
        app = xl.App(visible=False, add_book=False)
        try:
            app.display_alerts = False
            wb = app.books.open(target_file)
            try:
                sheet = wb.sheets[sheet_name]
                row_begin = start_row + 1
                row_end = start_row + df_len
                column_begin = 1
                column_end = df_column
                rng = sheet.range((row_begin, column_begin), (row_end, column_end))
                # 隐藏0 保留小数位0
                rng.number_format = '[=0]"";0'
                rng.api.Borders(7).Weight = 2
                rng.api.Borders(7).LineStyle = 1
                rng.api.Borders(8).Weight = 2
                rng.api.Borders(8).LineStyle = 1
                rng.api.Borders(9).Weight = 2
                rng.api.Borders(9).LineStyle = 1
                rng.api.Borders(10).Weight = 2
                rng.api.Borders(10).LineStyle = 1
                rng.api.Borders(11).Weight = 2
                rng.api.Borders(11).LineStyle = 1
                rng.api.Borders(12).Weight = 2
                rng.api.Borders(12).LineStyle = 1
                # 有合计行 加粗 改背景颜色
                total_row_list = []
                merge_row_list = []
                val = ""
                for row in range(row_begin, row_end + 1):
                    for column in range(column_begin, column_end + 1):
                        if sheet.range((row, column)).value == "合计":
                            total_row_list.append(row)
                        if column == column_begin:
                            if row == row_begin:
                                val = sheet.range((row, column)).value
                                merge_row_list.append(row)
                            else:
                                if val != sheet.range((row, column)).value:
                                    merge_row_list.append(row)
                                    val = sheet.range((row, column)).value
                for row in total_row_list:
                    sheet.range((row, 1)).expand("right").color = 217, 217, 217
                    sheet.range((row, 1)).expand("right").font.bold = True
                # 有合计列 改背景颜色
                if row_begin - 1 > 0:
                    total_column_list = []
                    title_row = row_begin - 1
                    for column in range(column_begin, column_end + 1):
                        if sheet.range((title_row, column)).value == "合计":
                            total_column_list.append(column)
                    for column in total_column_list:
                        sheet.range((row_begin, column)).expand("down").color = 217, 217, 217
                # 合并第一列相同单元格
                merge_row_list.append(row_end + 1)
                for index, merge in enumerate(merge_row_list, start=1):
                    if index == len(merge_row_list):
                        break
                    merge_rng = sheet.range((merge_row_list[index - 1], 1), (merge_row_list[index] - 1, 1))
                    merge_rng.merge()
                    merge_rng.api.HorizontalAlignment = -4108
                    merge_rng.api.VerticalAlignment = -4108
                # 写入截止时间
                prefix_date = os.path.basename(target_file)[:6]
                last_day = calendar.monthrange(int(prefix_date[:4]), int(prefix_date[4:6]))[1]
                last = prefix_date[:4] + r"/" + prefix_date[4:6] + "/" + str(last_day)
                date_location_list = self["date_location"].split(",")
                date_rng = sheet.range((int(date_location_list[0]), int(date_location_list[1])))
                date_rng.value = last
                date_rng.font.bold = True
                date_rng.font.size = 14
                date_rng.font.name = "微软雅黑"
            finally:
                wb.save()
                wb.close()
        finally:
            app.quit()
            app.kill()
            pythoncom.CoUninitialize()
