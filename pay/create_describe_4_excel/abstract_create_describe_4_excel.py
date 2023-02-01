# @Time    : 22/12/29 14:25
# @Author  : fyq
# @File    : abstract_create_describe_4_excel.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import abstractmethod

import typing
from pandas import DataFrame

from pay.attribute import AttributeManager
from pay.create_describe_4_excel.create_describe_4_excel import CreateDescribe4Excel
from pay.create_describe_4_excel.describe_excel import DescribeExcel


class AbstractCreateDescribe4Excel(CreateDescribe4Excel):

    def create_describe_4_excel(self, df_list: typing.List[DataFrame],
                                attribute_manager: AttributeManager) -> typing.List[DescribeExcel]:
        write_sheet_list = self.write_sheet_list(attribute_manager)
        describe_excel_list = []
        for index, df in enumerate(df_list):
            if df is None:
                continue
            de = self.new_describe_excel()
            write_sheet = write_sheet_list[index] if len(write_sheet_list) - 1 >= index else write_sheet_list[
                len(write_sheet_list) - 1]
            self._do_create_describe_4_excel(de=de,
                                             df=df,
                                             write_sheet=write_sheet,
                                             index=index,
                                             attribute_manager=attribute_manager)
            describe_excel_list.append(de)

        return describe_excel_list

    @abstractmethod
    def write_sheet_list(self, attribute_manager: AttributeManager):
        pass

    @abstractmethod
    def new_describe_excel(self) -> DescribeExcel:
        pass

    @abstractmethod
    def _do_create_describe_4_excel(self,
                                    de: DescribeExcel,
                                    df: DataFrame,
                                    write_sheet: str,
                                    index: int,
                                    attribute_manager: AttributeManager) -> None:
        pass
