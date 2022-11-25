# @Time    : 22/11/14 14:30
# @Author  : fyq
# @File    : green_sample_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.file_parser.map import ReconciliationFileParser
import pay.constant as pc
import re
import pandas as pd
import numpy as np


class GreenSampleMaterialFeeFileParser(ReconciliationFileParser):
    """
        绿洲样品材料费
    """

    def _after_parse_map(self, df, attribute_manager):
        material_name_column, qty_column, price_column = list(
            str(attribute_manager.value(pc.map_spec_column)).split(","))
        df[price_column].fillna(0, inplace=True)
        df[qty_column].fillna(0, inplace=True)
        df[material_name_column].fillna("", inplace=True)

        def handle_material_name(val):
            pattern = re.compile(r"(\d{3}[Gg])")
            res = re.search(pattern, val)
            if res:
                return res.group().upper()
            else:
                return val

        def handle_qty(row):
            if row[price_column] == 0:
                return 0
            else:
                return row[qty_column]

        def handle_money(row):
            return row[price_column] * row[qty_column]

        map_bill_code = attribute_manager.value(pc.map_bill_code)
        df[pc.new_material_name] = df[material_name_column].apply(handle_material_name)
        df[pc.new_money] = df.apply(handle_money, axis=1)
        df[pc.new_qty] = df.apply(handle_qty, axis=1)
        df[pc.new_bill_code] = df[map_bill_code]

        first_df = df[[pc.new_bill_code, pc.new_material_name, pc.new_qty, pc.new_money, price_column]] \
            .groupby(by=[pc.new_bill_code, pc.new_material_name, price_column], as_index=False) \
            .sum()

        def second_df(map_df):
            return map_df[[pc.new_bill_code, pc.new_qty, pc.new_money, price_column]] \
                .groupby(by=[pc.new_bill_code, price_column], as_index=False) \
                .sum()

        return [[first_df, [pc.new_bill_code, pc.new_material_name]],
                [second_df, [pc.new_bill_code]]]

    def _after_parse_data(self, df, attribute_manager):
        material_name_column, material_spec_column, qty_column, unit_column, price_column = list(
            str(attribute_manager.value(pc.data_spec_column)).split(","))
        df[price_column].fillna(0, inplace=True)
        df[qty_column].fillna(0, inplace=True)
        df[material_name_column].fillna("", inplace=True)
        df[material_spec_column].fillna("", inplace=True)

        def handle_material_name(row):
            pattern = re.compile(r"(\d{3}[Gg])")
            res = re.search(pattern, row[material_spec_column])
            if res:
                return res.group().upper()
            else:
                return row[material_name_column]

        def handle_qty(row):
            if row[price_column] == 0:
                return 0
            else:
                return row[qty_column]

        def handle_money(row):
            return row[price_column] * row[qty_column]

        def handle_discount(row):
            if pd.isna(row[unit_column]) or pd.isna(row[qty_column]):
                return np.nan

            qty = row[qty_column]
            if row[unit_column] == "双":
                if qty >= 20:
                    return "20%"
                else:
                    return "100%"
            elif row[unit_column] == "YD":
                if qty <= 5:
                    return "100%"
                elif qty > 10:
                    return "30%"
                else:
                    return "50%"
            else:
                return np.nan

        def handle_discount_money(row):
            if pd.isna(row[pc.new_money]) or pd.isna(row[pc.new_discount]):
                return np.nan

            return round(float(row[pc.new_discount].replace("%", "")) * row[pc.new_money] / 100, 2)

        data_bill_code = attribute_manager.value(pc.data_bill_code)
        df[pc.new_bill_code] = df[data_bill_code]
        df[pc.new_material_name] = df.apply(handle_material_name, axis=1)
        df[pc.new_money] = df.apply(handle_money, axis=1)
        df[pc.new_qty] = df.apply(handle_qty, axis=1)
        df[pc.new_discount] = df.apply(handle_discount, axis=1)
        df[pc.new_discount_money] = df.apply(handle_discount_money, axis=1)

        return df

    def _after_merger(self, df_list, attribute_manager):
        if len(df_list) > 0:
            if df_list[0] is not None:
                label_list = [pc.new_bill_code, pc.new_money, pc.new_qty, pc.new_material_name]
                df_list[0].drop(labels=label_list,
                                axis=1,
                                inplace=True,
                                errors="ignore")

    def _modify_attribute_manager(self, map_df, data_df, attribute_manager):
        attribute_manager.get(pc.map_data).value = \
            pc.new_qty + ":" + pc.new_qty + ":1," \
            + pc.new_money + ":" + pc.new_money + ":1"

    def support(self, pay_type):
        return "绿洲样品-材料费" == pay_type

    def _doing_merger_modify(self, map_df_row, data_df, attribute_manager):
        material_name_column, qty_column, price_column = list(
            str(attribute_manager.value(pc.map_spec_column)).split(","))
        data_df[pc.new_price] = map_df_row[price_column]
