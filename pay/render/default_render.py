# @Time    : 22/09/28 8:56
# @Author  : fyq
# @File    : default_render.py
# @Software: PyCharm

__author__ = 'fyq'

import pythoncom
import xlwings as xl
from pay.render.render import Render


class DefaultRender(Render):

    def render(self, describe_excel_list, attribute_manager, target_file):
        pythoncom.CoInitialize()
        app = xl.App(visible=False, add_book=False)
        try:
            app.display_alerts = False
            for desc_index, describe_excel in enumerate(describe_excel_list):
                wb = app.books.open(target_file)
                try:
                    sheet = wb.sheets[describe_excel.sheet_name]
                    sheet.select()
                    row_begin = describe_excel.start_row + 1
                    row_end = describe_excel.start_row + describe_excel.row
                    if row_end < row_begin:
                        row_end = row_begin
                    column_begin = describe_excel.start_column + 1
                    column_end = describe_excel.start_column + describe_excel.column
                    if column_end < column_begin:
                        column_end = column_begin
                    rng = sheet.range((row_begin, column_begin), (row_end, column_end))
                    # 边框
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
                    # 千分位
                    for index, value in describe_excel.df.dtypes().items():
                        if "int" in value.name or "float" in value.name:
                            column_index = int(index + 1)
                            sheet.range((row_begin, column_index), (row_end, column_index)).number_format = \
                                '[=0]"";###,###.00'
                    self._other_render(excel_app=app,
                                       describe_excel=describe_excel,
                                       describe_index=desc_index,
                                       sheet=sheet,
                                       attribute_manager=attribute_manager,
                                       row_begin=row_begin,
                                       row_end=row_end,
                                       column_begin=column_begin,
                                       column_end=column_end)
                finally:
                    wb.save()
                    wb.close()
        finally:
            app.quit()
            app.kill()
            pythoncom.CoUninitialize()

    def _other_render(self, excel_app, describe_excel, describe_index, sheet, attribute_manager, row_begin, row_end, column_begin, column_end):
        pass
