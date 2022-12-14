# @Time    : 22/08/09 16:55
# @Author  : fyq
# @File    : abstract_default_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import pythoncom

from pay.attribute_checker.common_checker import CommonChecker
from pay.create_describe_4_excel.default_create_describe_4_excel import DefaultCreateDescribe4Excel
from pay.file_parser.abstract_file_parser import AbstractFileParser
from loguru import logger
import pay.constant as pc
import numpy as np
import pandas as pd
from abc import abstractmethod
import xlwings as xl
from pay.decorator.pay_log import PayLog


class AbstractDefaultFileParser(AbstractFileParser):

    def _ignore(self):
        return False

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
    def _parser_file_dict(self, file_dict, attribute_manager, ignore):
        df_dict = {}
        for key in file_dict:
            df_file = []
            for file in file_dict[key]:
                try:
                    logger.info("开始解析文件[%s]" % file)
                    # 解析文件
                    df = self._parser_file(key=key,
                                           file=file,
                                           attribute_manager=attribute_manager,
                                           ignore=ignore)
                    logger.info("结束解析文件[%s]" % file)
                except Exception as e:
                    raise Exception("解析文件[%s]失败:[%s]" % (file, str(e)))
                # 加入到队列中
                if df is not None:
                    df_file.append(df)
            if len(df_file) > 0:
                df_dict[key] = pd.concat(df_file)

        return df_dict

    @PayLog(node="解析DataFrame")
    def _parse_df_dict(self, df_dict, attribute_manager):
        return self._do_parse_df_dict(df_dict=df_dict,
                                      attribute_manager=attribute_manager)

    @abstractmethod
    def _do_parse_df_dict(self, df_dict, attribute_manager):
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
    def _create_describe_4_excel(self, df_parse_list, attribute_manager):
        return DefaultCreateDescribe4Excel(df_parse_list, attribute_manager)

    @PayLog(node="写入excel")
    def _write_excel(self, describe_excel_list, attribute_manager, target_file):
        target_sheet_list = list(pd.read_excel(io=target_file, sheet_name=None))
        with pd.ExcelWriter(target_file,
                            engine='openpyxl',
                            mode='a',
                            if_sheet_exists="overlay") as writer:
            for describe_excel in describe_excel_list:
                for ts in target_sheet_list:
                    if describe_excel.sheet_name == ts.strip():
                        describe_excel.sheet_name = ts
                        break
                describe_excel.df.to_excel(writer,
                                           startrow=describe_excel.start_row,
                                           startcol=describe_excel.start_column,
                                           sheet_name=describe_excel.sheet_name,
                                           header=None,
                                           index=None)

    @PayLog(node="渲染excel")
    def _render_target(self, describe_excel_list, attribute_manager, target_file):
        pythoncom.CoInitialize()
        app = xl.App(visible=False, add_book=False)
        try:
            app.display_alerts = False
            for desc_index, describe_excel in enumerate(describe_excel_list):
                wb = app.books.open(target_file)
                try:
                    check = attribute_manager.value(pc.check)
                    has_check = check and len(check) > 0
                    sheet = wb.sheets[describe_excel.sheet_name]
                    sheet.select()
                    row_begin = describe_excel.start_row + 1
                    row_end = describe_excel.start_row + describe_excel.row
                    column_begin = describe_excel.start_column + 1
                    column_end = describe_excel.start_column + describe_excel.column
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
                        total_rng = sheet.range((row_begin + row, column_begin), (row_begin + row, column_end))
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

                    # 打印设置
                    if desc_index == 0:
                        sheet.api.PageSetup.LeftHeader = '&"微软雅黑,常规"&12编号:&A'
                        sheet.api.PageSetup.RightHeader = '&"微软雅黑,常规"&12打印日期：&D'
                        sheet.api.PageSetup.CenterFooter = '&"微软雅黑,常规"&12第 &P 页，共 &N 页'
                        sheet.api.PageSetup.PaperSize = 8
                        sheet.api.PageSetup.Orientation = 2
                        sheet.api.PageSetup.TopMargin = 1.5 * 28.35
                        sheet.api.PageSetup.BottomMargin = 1 * 28.35
                        sheet.api.PageSetup.LeftMargin = 0.5 * 28.35
                        sheet.api.PageSetup.RightMargin = 0.5 * 28.35
                        sheet.api.PageSetup.HeaderMargin = 0.8 * 28.35
                        sheet.api.PageSetup.FooterMargin = 0.5 * 28.35
                        sheet.api.PageSetup.CenterHorizontally = True
                        sheet.api.PageSetup.PrintTitleRows = "$1:$6"
                        sheet.api.PageSetup.Zoom = 100
                        sheet.api.PageSetup.PrintArea = \
                            "$" + CommonChecker.get_excel_column(describe_excel.start_column) + "$1" + ":$" + \
                            CommonChecker.get_excel_column(column_end - 2 if has_check else column_end - 1) + \
                            str(row_end)
                        app.api.ActiveWindow.View = 2
                finally:
                    wb.save()
                    wb.close()
        finally:
            app.quit()
            app.kill()
            pythoncom.CoUninitialize()

    def _write_sheet_list(self, attribute_manager):
        return [attribute_manager.value(pc.write_sheet)]

    def _parser_file(self, key, file, attribute_manager, ignore):
        df = None
        read_sheet = attribute_manager.value(pc.read_sheet)
        df_read_dict = pd.read_excel(io=file,
                                     sheet_name=None,
                                     skiprows=attribute_manager.value(pc.skip_rows),
                                     header=None,
                                     dtype=str)
        for sheet_name in df_read_dict.keys():
            if sheet_name.strip() == read_sheet or sheet_name.strip() == read_sheet + "-" + key:
                df = df_read_dict[sheet_name]
                break

        if df is None:
            if ignore:
                return None
            else:
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
        # 替换0为NAN
        df.replace(0, np.nan, inplace=True)
        # 去除全部NAN行
        df.dropna(axis=0, how="all", inplace=True)
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
            df[group_column].fillna("", inplace=True)
            df[group_column] = df[group_column].astype(str)
            df[group_column].str.strip()
            df.drop(df[df[group_column].isin(["小计", "合计", "总计"]) | (df[group_column].str.contains("汇总"))].index,
                    inplace=True)

    def _handler_data_column(self, df, attribute_manager):
        try:
            for column in df.columns:
                if str(column) not in self._group_column(attribute_manager=attribute_manager):
                    df[column] = df[column].apply(lambda x: "0" if str(x).isspace() else x)
                    df[column].fillna(0, inplace=True)
                    df[column] = df[column].astype("float64")
        except Exception as e:
            raise Exception("转换类型为浮点型失败,请检查解析文件是否存在非数字类型或者读取了标题行")

    @abstractmethod
    def _group_column(self, attribute_manager):
        """
            返回聚合列
        :param attribute_manager:
        :return: list
        """
        pass
