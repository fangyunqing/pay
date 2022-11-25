# @Time    : 22/11/11 15:07
# @Author  : fyq
# @File    : default_check_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import sys

from pay.create_describe_4_excel.default_create_describe_4_excel import DefaultCreateDescribe4Excel
from pay.file_parser.check.abstract_check_file_parser import AbstractCheckFileParser
from pay.render.default_render import DefaultRender
from pay.reset_index.default_reset_index import DefaultResetIndex
from pay.write_excel.default_write_excel import DefaultWriteExcel
import pay.constant as pc
import pandas as pd
from util import pd_read_excel
import numpy as np
from itertools import combinations


class DefaultCheckFileParser(AbstractCheckFileParser):
    MEMO = "memo"

    def _do_parse_data(self, file_dict, target_file, attribute_manager):
        data_file_info = str(attribute_manager.value(pc.data_file)).split(",")
        use_column_list = list(attribute_manager.value(pc.use_column).split(","))
        df = pd_read_excel(data_file_info, file_dict, use_column_list)
        check_data_list = str(attribute_manager.value(pc.check_data)).split(",")
        group_column = str(attribute_manager.value(pc.group_column)).split(",")
        check_result_list = str(attribute_manager.value(pc.check_result)).split(",")
        sort_column = str(attribute_manager.value(pc.sort_column))
        sort_column_list = group_column.copy()
        sort_column_list.append(sort_column)
        # 排序列
        df.sort_values(by=sort_column_list, inplace=True)
        df.index = range(0, len(df.index))
        # 增加列
        for site in range(0, len(check_data_list)):
            df[self.MEMO + str(site)] = ""
            df[self.MEMO + str(site) + "-1"] = ""
        # 根据列分组
        group = df.groupby(group_column, as_index=False)
        for group_key in group.groups.keys():
            line_list = group.groups[group_key]
            for check_data_index, check_data in enumerate(check_data_list):
                c_list = check_data.split(":")
                c_left = c_list[0]
                c_right = c_list[1]
                right_value = np.nan
                left_value_list = []
                for line in line_list:
                    if not pd.isna(df.loc[line, c_right]):
                        right_value = df.loc[line, c_right]
                    left_value_list.append(df.loc[line, c_left])
                # 有差值
                if not pd.isna(right_value):
                    index_list = list(range(1, len(line_list) + 1))
                    times_list = index_list.copy()
                    if len(line_list) > 15:
                        times_list = list(range(1, 8))
                    combination_result = []
                    for index in times_list:
                        for combination in combinations(index_list, index):
                            combination_sum = 0
                            combination_sum_map = []
                            for combination_element in combination:
                                combination_sum = combination_sum + left_value_list[combination_element - 1]
                                combination_sum_map.append(line_list[combination_element - 1])
                            if (round(combination_sum, 6) + round(right_value, 6)) == 0:
                                combination_result.append(combination_sum_map)
                    if len(combination_result) > 0:
                        for combination in combination_result:
                            if len(combination) < len(line_list):
                                for site in range(0, len(line_list) - len(combination)):
                                    combination.insert(0, sys.maxsize)
                        combination_df = pd.DataFrame(data=combination_result,
                                                      columns=range(0, len(line_list)))
                        combination_df.sort_values(by=list(reversed(range(0, len(line_list)))),
                                                   ascending=[False for r in range(0, len(line_list))],
                                                   inplace=True)
                        for row_index in combination_df.iloc[0]:
                            if row_index != sys.maxsize:
                                df.loc[row_index, self.MEMO + str(check_data_index)] = check_result_list[0]
                        df.loc[line_list[0], self.MEMO + str(check_data_index) + "-1"] = check_result_list[0]
                    else:
                        find = False
                        for left_index, left_value in enumerate(left_value_list[::-1]):
                            if round(left_value, 6) + round(right_value, 6) > 0:
                                find = True
                                df.loc[line_list[::-1][left_index], self.MEMO + str(check_data_index)] = \
                                    check_result_list[1]
                                df.loc[line_list[0], self.MEMO + str(check_data_index) + "-1"] = check_result_list[1]
                                break
                        if not find:
                            df.loc[line_list[0], self.MEMO + str(check_data_index)] = \
                                "未找到"
                            df.loc[line_list[0], self.MEMO + str(check_data_index) + "-1"] = "未找到"

        return [df]

    def _do_create_describe_4_excel(self, df, attribute_manager):
        return DefaultCreateDescribe4Excel().create_describe_4_excel(df_list=df,
                                                                     attribute_manager=attribute_manager)

    def _do_write_excel(self, describe_excel, attribute_manager, target_file):
        DefaultWriteExcel().write_excel(describe_excel, attribute_manager, target_file)

    def _do_render_target(self, describe_excel_list, attribute_manager, target_file):
        DefaultRender().render(describe_excel_list, attribute_manager, target_file)

    def support(self, pay_type):
        return True

    def _do_reset_index(self, df, attribute_manager):
        DefaultResetIndex().reset_index(df, attribute_manager)
