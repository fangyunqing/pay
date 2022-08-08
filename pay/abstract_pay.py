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

    def __init__(self):
        self.attribute_dict = {}
        self.dept_column = "dept"
        self.check_column = "check"
        self.first_merge = False
        # 属性字段
        self.read_sheet = "read_sheet"
        self.skip_rows = "skip_rows"
        self.use_column = "use_column"
        self.sort_column = "sort_column"
        self.supplier_column = "supplier_column"
        self.type_column = "type_column"
        self.write_sheet = "write_sheet"
        self.date_location = "date_location"
        self.check = "check"
        self.attribute_list = [
            {
                "name": "read_sheet",
                "text": "读取的工作簿名称",
                "type": "str"
            },
            {
                "name": "skip_rows",
                "text": "跳过的行数",
                "type": "int"
            },
            {
                "name": "use_column",
                "text": "需要的列(从0开始,逗号分隔)",
                "type": "str"
            },
            {
                "name": "sort_column",
                "text": "排序列",
                "type": "int"
            },
            {
                "name": "supplier_column",
                "text": "供应商列号",
                "type": "int"
            },
            {
                "name": "type_column",
                "text": "供应商类型列号",
                "type": "int"
            },
            {
                "name": "write_sheet",
                "text": "写入的工作簿名称",
                "type": "str"
            },
            {
                "name": "date_location",
                "text": "截止时间位置(从0开始,行列 eg:3,4)",
                "type": "str"
            },
            {
                "name": "check",
                "text": "校对",
                "type": "str"
            },
        ]
        # 描述字段
        self._df = "df"
        self._start_row = "start_row"
        self._row = "row"
        self._column = "column"
        self._total_row = "total_row"
        self._first_row_index = "first_row_index"
        self._sheet_name = "sheet_name"
        self._target_file = "target_file"
        self._detail = "detail"

    def __getitem__(self, item):
        try:
            return self.attribute_dict[item]
        except KeyError:
            return None

    @staticmethod
    def get_supplier_useless_field():
        return ["小计", "合计", "", np.nan]

    @abstractmethod
    def _parse(self, df_dict):
        pass

    def _write_excel(self, target_file, df_describe_list):
        with pd.ExcelWriter(target_file, engine='openpyxl', mode='a', if_sheet_exists="overlay") as writer:
            for df_describe in df_describe_list:
                df_describe[self._df].to_excel(writer,
                                               startrow=df_describe[self._start_row],
                                               sheet_name=df_describe[self._sheet_name],
                                               header=None,
                                               index=None)

    def parse(self, file_dict, target_file):
        pd.set_option('display.max_columns', None)
        df_dict = {}
        for key in file_dict:
            dept_file = []

            for file in file_dict[key]:
                df = None
                df_read_dict = pd.read_excel(file, sheet_name=None, skiprows=self["skip_rows"], header=None)
                for sheet_name in df_read_dict.keys():
                    if sheet_name.strip() == self["read_sheet"] or sheet_name.strip() == self["read_sheet"] + "-" + key:
                        df = df_read_dict[sheet_name]
                        break

                if df is None:
                    raise Exception("[%s]中无法找工作簿[%s]" % (file, self["read_sheet"]))

                useless_column = []
                for value in df.columns:
                    if str(value) not in self["use_column"]:
                        useless_column.append(value)
                # 去除空格
                df[self["supplier_column"]] = df[self["supplier_column"]].astype(str)
                df[self["type_column"]] = df[self["type_column"]].astype(str)
                df[self["supplier_column"]].str.strip()
                df[self["type_column"]].str.strip()
                # 去除供应商无用的行
                df.drop(df[df[self["supplier_column"]].isin(self.get_supplier_useless_field())].index,
                        inplace=True)
                # 去除type中无用的行
                df.drop(df[(df[self["type_column"]] == "总计") | (df[self["type_column"]].str.contains("汇总"))].index,
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
                df_dict[key] = pd.concat(dept_file)

        # 解析
        df_parse_list = self._parse(df_dict)
        # 重新索引
        for df_parse in df_parse_list:
            df_parse.columns = range(0, len(df_parse.columns))
            df_parse.index = range(0, len(df_parse.index))
        # 插入校对
        self._insert_check(df_parse_list)
        # 描述
        df_describe_list = self._describe(df_parse_list, target_file)
        # 写入excel
        self._write_excel(target_file, df_describe_list)
        # 渲染
        self._set_style(df_describe_list)

    def _set_style(self, df_describe_list):
        pythoncom.CoInitialize()
        app = xl.App(visible=False, add_book=False)
        try:
            app.display_alerts = False
            for df_describe in df_describe_list:
                wb = app.books.open(df_describe[self._target_file])
                try:
                    sheet = wb.sheets[df_describe[self._sheet_name]]
                    row_begin = df_describe[self._start_row] + 1
                    row_end = df_describe[self._start_row] + df_describe[self._row]
                    column_begin = 1
                    column_end = df_describe[self._column] if not self._has_check() else df_describe[self._column] - 1
                    column_all = df_describe[self._column]
                    rng = sheet.range((row_begin, column_begin), (row_end, column_all))
                    # 隐藏0 保留小数位0
                    rng.number_format = '[=0]"";###,###'
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
                    for row in df_describe[self._total_row]:
                        total_rng = sheet.range((row_begin + row, 1), (row_begin + row, column_end))
                        total_rng.color = 217, 217, 217
                        total_rng.font.bold = True
                    # 有合计列 改背景颜色
                    if row_begin - 1 > 0:
                        total_column_list = []
                        title_row = row_begin - 1
                        for column in range(column_begin, column_end + 1):
                            if sheet.range((title_row, column)).value == "合计":
                                total_column_list.append(column)
                        for column in total_column_list:
                            sheet.range((row_begin, column)).expand("down").color = 217, 217, 217
                    # 第一行是否合并
                    if self.first_merge:
                        r = row_begin
                        for ri in df_describe[self._first_row_index]:
                            e = r + ri
                            merge_rng = sheet.range((r, 1), (e - 1, 1))
                            merge_rng.merge()
                            merge_rng.api.HorizontalAlignment = -4108
                            merge_rng.api.VerticalAlignment = -4108
                            r = e
                    # 写入截止时间
                    prefix_date = os.path.basename(df_describe[self._target_file])[:6]
                    last_day = calendar.monthrange(int(prefix_date[:4]), int(prefix_date[4:6]))[1]
                    last = prefix_date[:4] + r"/" + prefix_date[4:6] + "/" + str(last_day)
                    date_location_list = self["date_location"].split(",")
                    dx = int(date_location_list[0]) + 1
                    dy = int(date_location_list[1]) + 2 if df_describe[self._detail] else int(date_location_list[1]) + 1
                    date_rng = sheet.range((dx, dy))
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

    def sort(self, df):
        sort_column = self["sort_column"]
        if sort_column is not None and sort_column != "":
            df.sort_values(sort_column, ascending=False, inplace=True)

    def _insert_check(self, df_list):
        df = df_list[0]
        if self._has_check():
            check = self["check"]
            df[self.check_column] = 0
            check_list = list(check.split(","))
            for c in check_list:
                s_list = list(c.split("-"))
                s_list = [int(s) for s in s_list]
                if len(s_list) > 1:
                    df[self.check_column] = df[self.check_column] + df[s_list[0]]
                    for s in s_list[1:]:
                        df[self.check_column] = df[self.check_column] - df[s]
            df[self.check_column] = df[self.check_column].round(4)

    def _has_check(self):
        check = self["check"]
        return check is not None and check != ""

    def _describe(self, df_list, target_file):
        sheet_info_list = self._sheet_info()
        df_describe_list = []
        for index, df in enumerate(df_list):

            # 合计行
            total_row = []
            for row_index, row in df.iterrows():
                for r in row:
                    if r == "合计":
                        total_row.append(row_index)
                        break
            # 第一列
            first_row_index = []
            vc = df[0].value_counts()
            for v in df[0].unique():
                first_row_index.append(vc[v])

            detail = True if index > 0 else False

            sheet_info = sheet_info_list[index]
            df_describe = {self._df: df,
                           self._row: len(df.index),
                           self._column: len(df.columns),
                           self._sheet_name: sheet_info[0],
                           self._start_row: sheet_info[1],
                           self._target_file: target_file,
                           self._total_row: total_row,
                           self._first_row_index: first_row_index,
                           self._detail: detail}
            df_describe_list.append(df_describe)
        return df_describe_list

    def _sheet_info(self):
        sheet_name, start_row = self["write_sheet"].split(",")
        return [(sheet_name, int(start_row))]

    @abstractmethod
    def pay_name(self):
        pass

    @abstractmethod
    def pay_options(self):
        pass

    def _insert_attribute(self, attribute_name, attribute):
        find_index = [index for index, attribute in enumerate(self.attribute_list)
                      if attribute["name"] == attribute_name]
        if len(find_index) > 0:
            self.attribute_list.insert(find_index[0], attribute)
