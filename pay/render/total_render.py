# @Time    : 22/12/29 16:28
# @Author  : fyq
# @File    : total_render.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.render.default_render import DefaultRender


class TotalRender(DefaultRender):

    def _other_render(self, describe_excel, sheet, attribute_manager):
        # 有合计行 加粗 改背景颜色
        for row in describe_excel.total_row:
            total_rng = sheet.range((row_begin + row, column_begin), (row_begin + row, column_end))
            total_rng.color = 217, 217, 217
            total_rng.font.bold = True