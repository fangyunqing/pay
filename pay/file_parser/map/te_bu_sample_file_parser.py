# @Time    : 22/11/16 14:09
# @Author  : fyq
# @File    : te_bu_sample_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.file_parser.map import ReconciliationFileParser
import pay.constant as pc
import pandas as pd
import re


class TeBuSampleFileParser(ReconciliationFileParser):
    NEW_MATERIAL_NAME = "new_material_name"

    def _after_parse_map(self, df, attribute_manager):

        material_name_column, color, qty, price, money = list(
            str(attribute_manager.value(pc.map_spec_column)).split(","))

        def handle_material_name(row):

            if pd.isna(row[material_name_column]):
                return row[material_name_column]

            pattern = re.compile(r"(HF[a-zA-Z\d\-\s]{8})")
            res = re.search(pattern, row[material_name_column])
            if res:
                return res.group().upper().replace(" ", "")
            elif row[material_name_column].startswith("小高弹"):
                return "小高弹"
            elif row[material_name_column].startswith("消光圆点"):
                return "消光圆点"
            else:
                return row[material_name_column]

        map_bill_code = attribute_manager.value(pc.map_bill_code)
        df[pc.new_bill_code] = df[map_bill_code]
        df[pc.new_material_name] = df.apply(handle_material_name, axis=1)
        df[pc.new_color] = df[color]

        first_df = df[[pc.new_bill_code, pc.new_material_name, pc.new_color, qty, price, money]] \
            .groupby(by=[pc.new_bill_code, pc.new_material_name, pc.new_color, price], as_index=False) \
            .sum()

        def second_df(map_df):
            return map_df[[pc.new_bill_code, pc.new_color, qty, price, money]] \
                .groupby(by=[pc.new_bill_code, pc.new_color, price], as_index=False) \
                .sum()

        return [[first_df, [pc.new_bill_code, pc.new_material_name, pc.new_color]],
                [second_df, [pc.new_bill_code, pc.new_color]]]

    def _after_parse_data(self, df, attribute_manager):
        color, material_name_column, qty, price, money = list(
            str(attribute_manager.value(pc.data_spec_column)).split(","))

        def handle_material_name(row):

            if pd.isna(row[material_name_column]):
                return row[material_name_column]

            pattern = re.compile(r"(HF[a-zA-Z\d\-\s]{8})")
            res = re.search(pattern, row[material_name_column])
            if res:
                return res.group().upper().replace(" ", "")
            elif row[material_name_column].startswith("小高弹"):
                return "小高弹"
            elif row[material_name_column].startswith("消光圆点"):
                return "消光圆点"
            else:
                return row[material_name_column]

        data_bill_code = attribute_manager.value(pc.data_bill_code)
        df[pc.new_bill_code] = df[data_bill_code]
        df[pc.new_material_name] = df.apply(handle_material_name, axis=1)
        df[pc.new_color] = df[color]

        return df

    def support(self, pay_type):
        return "特步样品" == pay_type

    def _after_merger(self, df_list, attribute_manager):
        if len(df_list) > 0:
            if df_list[0] is not None:
                label_list = [pc.new_bill_code, pc.new_material_name, pc.new_color]
                df_list[0].drop(labels=label_list,
                                axis=1,
                                inplace=True,
                                errors="ignore")
