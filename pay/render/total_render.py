# @Time    : 23/02/01 11:25
# @Author  : fyq
# @File    : total_render.py
# @Software: PyCharm

__author__ = 'fyq'

from xlwings import Sheet, App

from pay.attribute import AttributeManager
from pay.attribute_checker.common_checker import CommonChecker
from pay.create_describe_4_excel.describe_excel import DescribeExcel, TotalDescribeExcel
from pay.render.default_render import DefaultRender
from pay.constant import attr_string
import pay.constant as pc


class TotalRender(DefaultRender):

    def _do_render(self,
                   attribute_manager: AttributeManager,
                   desc_index: int, describe_excel: DescribeExcel,
                   row_begin: int, row_end: int,
                   column_begin: int, column_end: int,
                   app: App, sheet: Sheet):
        super()._do_render(desc_index, describe_excel, row_begin, row_end, column_begin, column_end, app, sheet)
        if isinstance(describe_excel, TotalDescribeExcel):
            # 有合计行 加粗 改背景颜色
            for total_row in describe_excel.total_row_list:
                total_rng = sheet.range((row_begin + total_row, column_begin), (row_begin + total_row, column_end))
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
            # 首列合并
            first_column_merger = attribute_manager.value(attr_string.first_column_merger)
            if first_column_merger == 1:
                r = row_begin
                for ri in describe_excel.first_column_merger_list:
                    e = r + ri
                    merge_rng = sheet.range((r, 1), (e - 1, 1))
                    merge_rng.merge()
                    merge_rng.api.HorizontalAlignment = -4108
                    merge_rng.api.VerticalAlignment = -4108
                    r = e
            # 打印设置
            check = attribute_manager.value(pc.check)
            has_check = check and len(check) > 0
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
