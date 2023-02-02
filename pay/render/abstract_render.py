# @Time    : 23/02/01 10:43
# @Author  : fyq
# @File    : abstract_render.py
# @Software: PyCharm

__author__ = 'fyq'

import typing
from abc import abstractmethod

import pythoncom
from xlwings import Sheet, App

from pay.attribute import AttributeManager
from pay.create_describe_4_excel.describe_excel import DescribeExcel
import xlwings as xl
from pay.render.render import Render


class AbstractRender(Render):

    @abstractmethod
    def _do_render(self,
                   attribute_manager: AttributeManager,
                   desc_index: int,
                   describe_excel: DescribeExcel,
                   row_begin: int, row_end: int,
                   column_begin: int, column_end: int,
                   app: App,
                   sheet: Sheet):
        pass

    def render(self, describe_excel_list: typing.List[DescribeExcel], attribute_manager: AttributeManager,
               target_file: str) -> None:
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
                    row_end = describe_excel.start_row + describe_excel.row_count
                    if row_end < row_begin:
                        row_end = row_begin
                    column_begin = describe_excel.start_column + 1
                    column_end = describe_excel.start_column + describe_excel.column_count
                    if column_end < column_begin:
                        column_end = column_begin
                    self._do_render(attribute_manager=attribute_manager,
                                    desc_index=desc_index,
                                    describe_excel=describe_excel,
                                    row_begin=row_begin, row_end=row_end,
                                    column_begin=column_begin, column_end=column_end,
                                    app=app, sheet=sheet)
                finally:
                    wb.save()
                    wb.close()
        finally:
            app.quit()
            app.kill()
            pythoncom.CoUninitialize()
