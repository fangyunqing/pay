# @Time    : 22/08/09 16:55
# @Author  : fyq
# @File    : abstract_default_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import pythoncom

from pay.file_parser.abstract_file_parser import AbstractFileParser
from loguru import logger
import pay.constant as pc
import numpy as np
import pandas as pd
from abc import abstractmethod
from pay.describe_excel import DescribeExcel
import xlwings as xl
from pay.decorator.pay_log import PayLog


class AbstractDefaultFileParser(AbstractFileParser):

    def __init__(self):
        # 第一列是否需要合并
        self._first_merge = False
        # 校对列
        self._check_column = "check"
        # 名称列
        self._name_column = "name"
        # 是否插入名称列
        self._insert_name = True

    @PayLog(node="解析文件")
    def _parser_file_dict(self, file_dict, attribute_manager):
        df_dict = {}
        for key in file_dict:
            df_file = []
            for file in file_dict[key]:
                try:
                    logger.info("开始解析文件[%s]" % file)
                    # 解析文件
                    df = self._parser_file(key=key,
                                           file=file,
                                           attribute_manager=attribute_manager)
                    logger.info("结束解析文件[%s]" % file)
                except Exception as e:
                    raise Exception("解析文件[%s]失败:[%s]" % (file, str(e)))
                # 加入到队列中
                df_file.append(df)
            if len(df_file) > 0:
                df_dict[key] = pd.concat(df_file)

        return df_dict

    @abstractmethod
    def _parse_df_dict(self, df_dict, attribute_manager):
        pass

    @PayLog(node="重建索引")
    def _reset_index(self, df_parse_list, attribute_manager):
        for df_parse in df_parse_list:
            df_parse.columns = [str(r) for r in range(0, len(df_parse.columns))]
            df_parse.index = range(0, len(df_parse.index))

    @PayLog(node="校对")
    def _check(self, df_parse_list, attribute_manager):
        check = attribute_manager.value(pc.check)
        if check and len(check) > 0:
            df_parse = df_parse_list[0]
            df_parse[self._check_column] = 0
            check_exp_list = list(check.split(","))
            for check_exp in check_exp_list:
                check_list = list(check_exp.split("-"))
                check_list = [s for s in check_list]
                if len(check_list) > 1:
                    df_parse[self._check_column] = df_parse[self._check_column] + df_parse[check_list[0]]
                    for c in check_list[1:]:
                        df_parse[self._check_column] = df_parse[self._check_column] - df_parse[c]
            df_parse[self._check_column] = df_parse[self._check_column].round(4)

    @PayLog(node="创建excel描述")
    def _create_describe_4_excel(self, df_parse_list, attribute_manager, target_file):
        write_sheet_list = self._write_sheet_list(attribute_manager)
        describe_excel_list = []
        for index, df_parse in enumerate(df_parse_list):
            # 合计行
            total_row_list = []
            for row_index, row in df_parse.iterrows():
                for cell in row:
                    if cell == "合计":
                        total_row_list.append(row_index)
                        break
            # 第一列
            first_row_index = []
            vc = df_parse['0'].value_counts()
            for v in df_parse['0'].unique():
                first_row_index.append(vc[v])

            write_sheet = write_sheet_list[index]
            write_sheet_info = list(write_sheet.split(","))
            describe_excel = DescribeExcel()
            describe_excel.df = df_parse
            describe_excel.row = len(df_parse.index)
            describe_excel.column = len(df_parse.columns)
            describe_excel.sheet_name = write_sheet_info[0]
            describe_excel.start_row = int(write_sheet_info[1])
            describe_excel.target_file = target_file
            describe_excel.total_row = total_row_list
            describe_excel.first_row_index = first_row_index
            describe_excel.detail = True if index > 0 else False
            describe_excel_list.append(describe_excel)
        return describe_excel_list

    @PayLog(node="写入excel")
    def _write_excel(self, describe_excel_list, attribute_manager):
        for describe_excel in describe_excel_list:
            with pd.ExcelWriter(describe_excel.target_file,
                                engine='openpyxl',
                                mode='a',
                                if_sheet_exists="overlay") as writer:
                describe_excel.df.to_excel(writer,
                                           startrow=describe_excel.start_row,
                                           sheet_name=describe_excel.sheet_name,
                                           header=None,
                                           index=None)

    @PayLog(node="渲染excel")
    def _render_target(self, describe_excel_list, attribute_manager):
        pythoncom.CoInitialize()
        app = xl.App(visible=False, add_book=False)
        try:
            app.display_alerts = False
            for describe_excel in describe_excel_list:
                wb = app.books.open(describe_excel.target_file)
                try:
                    sheet = wb.sheets[describe_excel.sheet_name]
                    row_begin = describe_excel.start_row + 1
                    row_end = describe_excel.start_row + describe_excel.row
                    column_begin = 1
                    column_end = describe_excel.column
                    rng = sheet.range((row_begin, column_begin), (row_end, column_end))
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
                    rng.font.size = 12
                    rng.font.name = "微软雅黑"
                    # 有合计行 加粗 改背景颜色
                    for row in describe_excel.total_row:
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
                    if self._first_merge:
                        r = row_begin
                        for ri in describe_excel.first_row_index:
                            e = r + ri
                            merge_rng = sheet.range((r, 1), (e - 1, 1))
                            merge_rng.merge()
                            merge_rng.api.HorizontalAlignment = -4108
                            merge_rng.api.VerticalAlignment = -4108
                            r = e
                finally:
                    wb.save()
                    wb.close()
        finally:
            app.quit()
            app.kill()
            pythoncom.CoUninitialize()

    def _write_sheet_list(self, attribute_manager):
        return [attribute_manager.value(pc.write_sheet)]

    def _parser_file(self, key, file, attribute_manager):
        df = None
        read_sheet = attribute_manager.value(pc.read_sheet)
        df_read_dict = pd.read_excel(io=file,
                                     sheet_name=None,
                                     skiprows=attribute_manager.value(pc.skip_rows),
                                     header=None)
        for sheet_name in df_read_dict.keys():
            if sheet_name.strip() == read_sheet or sheet_name.strip() == read_sheet + "-" + key:
                df = df_read_dict[sheet_name]
                break

        if df is None:
            raise Exception("[%s]中无法找工作簿[%s]" % (file, read_sheet))

        # 列索引转换为字符串
        df.columns = [str(column) for column in df.columns]
        useless_column = []
        use_column_list = list(attribute_manager.value(pc.use_column).split(","))
        for value in df.columns:
            if value not in use_column_list:
                useless_column.append(value)
        # 去除无用的列
        if len(useless_column) > 0:
            df.drop(useless_column, axis=1, inplace=True, errors="ignore")
        # 聚合数据清理
        self._handle_group_column(df=df, attribute_manager=attribute_manager)
        # 非聚合数据清理
        self._handler_data_column(df=df, attribute_manager=attribute_manager)
        # 插入名称在第一列
        if self._insert_name:
            df.insert(column=self._name_column, value=key, loc=0)

        return df

    def _handle_group_column(self, df, attribute_manager):
        for group_column in self._group_column(attribute_manager):
            df.drop(df[df[group_column].isin(["小计", "合计", "", np.nan]) | (df[group_column].str.contains("汇总"))].index,
                    inplace=True)
            df[group_column] = df[group_column].astype(str)
            df[group_column].str.strip()

    def _handler_data_column(self, df, attribute_manager):
        try:
            df.fillna(0, inplace=True)
            for column in df.columns:
                if str(column) not in self._group_column(attribute_manager=attribute_manager):
                    df[column] = df[column].astype("float64")
        except Exception:
            raise Exception("转换类型为浮点型失败,请检查解析文件是否存在非数字类型或者读取了标题行")

    @abstractmethod
    def _group_column(self, attribute_manager):
        """
            返回聚合列
        :param attribute_manager:
        :return: list
        """
        pass

