# @Time    : 22/09/28 8:56
# @Author  : fyq
# @File    : default_render.py
# @Software: PyCharm

__author__ = 'fyq'

import pythoncom
import typing
import xlwings as xl
from xlwings import Sheet

from pay.attribute import AttributeManager
from pay.create_describe_4_excel.describe_excel import DescribeExcel
from pay.render.abstract_render import AbstractRender


class DefaultRender(AbstractRender):

    def _do_render(self, desc_index: int, describe_excel: DescribeExcel, row_begin: int, row_end: int,
                   column_begin: int, column_end: int, sheet: Sheet):
        # 边框设置样式
        rng = sheet.range((row_begin, column_begin), (row_end, column_end))
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
        # 设置千分位
