# @Time    : 23/02/01 14:02
# @Author  : fyq
# @File    : abstract_common_payable_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import abstractmethod
from typing import Dict, Iterable, Optional, List

from loguru import logger
from pandas import DataFrame

from pay.attribute import AttributeManager
from pay.create_describe_4_excel import TotalCreateDescribe4Excel
from pay.create_describe_4_excel.describe_excel import DescribeExcel
from pay.file_parser.payable.abstract_payable_file_parser import AbstractPayableFileParser
import pandas as pd
import pay.constant as pc
import numpy as np
from pay.render import TotalRender
from pay.reset_index.default_reset_index import DefaultResetIndex
from pay.write_excel.default_write_excel import DefaultWriteExcel


class AbstractCommonPayableFileParser(AbstractPayableFileParser):

    def _do_create_describe_4_excel(self, df_list: List[DataFrame],
                                    attribute_manager: AttributeManager) -> List[DescribeExcel]:
        return TotalCreateDescribe4Excel().create_describe_4_excel(df_list=df_list,
                                                                   attribute_manager=attribute_manager)

    def _do_write_excel(self, describe_excel_list: List[DescribeExcel], attribute_manager: AttributeManager,
                        target_file: str):
        DefaultWriteExcel().write_excel(describe_excel_list, attribute_manager, target_file)

    def _do_render_target(self, describe_excel_list: List[DescribeExcel], attribute_manager: AttributeManager,
                          target_file: str):
        TotalRender().render(describe_excel_list=describe_excel_list,
                             attribute_manager=attribute_manager,
                             target_file=target_file)

    def _do_check(self, df_list: List[DataFrame], attribute_manager: AttributeManager):
        check = attribute_manager.value(pc.check)
        if check and len(check) > 0:
            df_parse = df_list[0]
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

    def _do_reset_index(self, df_list: List[DataFrame], attribute_manager: AttributeManager):
        DefaultResetIndex().reset_index(df_list, attribute_manager)

    def __init__(self):
        # 校对列
        self._check_column = "check"
        # 名称列
        self._name_column = "name"

    def _do_read_file(self, file_dict: Dict[str, Iterable], attribute_manager: AttributeManager,
                      ignore_not_exist: bool) -> Dict[str, DataFrame]:
        df_dict = {}
        for key in file_dict:
            df_file = []
            for file in file_dict[key]:
                try:
                    logger.info("开始解析文件[%s]" % file)
                    # 解析文件
                    df = self._read_excel(key=key,
                                          file=file,
                                          attribute_manager=attribute_manager,
                                          ignore=ignore_not_exist)
                    logger.info("结束解析文件[%s]" % file)
                except Exception as e:
                    raise Exception("解析文件[%s]失败:[%s]" % (file, str(e)))
                # 加入到队列中
                if df is not None:
                    df_file.append(df)
            if len(df_file) > 0:
                df_dict[key] = pd.concat(df_file)

        return df_dict

    def _read_excel(self, key: str, file: str,
                    attribute_manager: AttributeManager,
                    ignore: bool) -> Optional[DataFrame]:
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
        if self._insert_name():
            df.insert(column=self._name_column, value=key, loc=0)

        return df

    @abstractmethod
    def _insert_name(self) -> bool:
        pass

    def _handle_group_column(self, df: DataFrame, attribute_manager: AttributeManager):
        for group_column in self._group_column(attribute_manager):
            df[group_column].fillna("", inplace=True)
            df[group_column] = df[group_column].astype(str)
            df[group_column].str.strip()
            df.drop(df[df[group_column].isin(["小计", "合计", "总计"]) | (df[group_column].str.contains("汇总"))].index,
                    inplace=True)

    def _handler_data_column(self, df: DataFrame, attribute_manager: AttributeManager):
        try:
            for column in df.columns:
                if str(column) not in self._group_column(attribute_manager=attribute_manager):
                    df[column] = df[column].apply(lambda x: "0" if str(x).isspace() else x)
                    df[column].fillna(0, inplace=True)
                    df[column] = df[column].astype("float64")
        except Exception as e:
            raise Exception("转换类型为浮点型失败,请检查解析文件是否存在非数字类型或者读取了标题行")

    @abstractmethod
    def _group_column(self, attribute_manager) -> List:
        pass
