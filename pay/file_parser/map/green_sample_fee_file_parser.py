# @Time    : 22/11/25 11:55
# @Author  : fyq
# @File    : green_sample_fee_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.file_parser.map import ReconciliationFileParser
import pay.constant as pc
import numpy as np
import pandas as pd


class GreenSampleFeeFileParser(ReconciliationFileParser):

    def _after_parse_map(self, df, attribute_manager):
        material_name_column, qty_column, price_column, fee_column = list(
            str(attribute_manager.value(pc.map_spec_column)).split(","))
        df[fee_column].fillna(0, inplace=True)
        df[price_column].fillna(0, inplace=True)
        df[qty_column].fillna(0, inplace=True)
        df[material_name_column].fillna("", inplace=True)

        def handle_fee_count(row):
            return 1 if row[fee_column] != 0 else 0

        def handle_qty(row):
            if row[price_column] == 0:
                return 0
            else:
                return row[qty_column]

        def handle_money(row):
            return row[price_column] * row[qty_column]

        map_bill_code = attribute_manager.value(pc.map_bill_code)
        df[pc.new_bill_code] = df[map_bill_code]
        df[pc.new_fee_count] = df.apply(handle_fee_count, axis=1)
        df[pc.new_fee] = df[fee_column]
        df[pc.new_money] = df.apply(handle_money, axis=1)
        df[pc.new_qty] = df.apply(handle_qty, axis=1)

        first_df = df[[pc.new_bill_code, pc.new_money, pc.new_qty, price_column,
                       pc.new_fee_count, pc.new_fee]] \
            .groupby(by=[pc.new_bill_code, price_column], as_index=False) \
            .sum()

        return [[first_df, [pc.new_bill_code]]]

    def _after_parse_data(self, df, attribute_manager):
        material_name_column, material_spec_column, qty_column, unit_column, price_column, fee_column = list(
            str(attribute_manager.value(pc.data_spec_column)).split(","))
        df[price_column].fillna(0, inplace=True)
        df[qty_column].fillna(0, inplace=True)
        df[material_name_column].fillna("", inplace=True)
        df[material_spec_column].fillna("", inplace=True)
        df[fee_column].fillna(0, inplace=True)

        def handle_fee_count(row):
            return 1 if row[fee_column] != 0 else 0

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
        df[pc.new_money] = df.apply(handle_money, axis=1)
        df[pc.new_qty] = df.apply(handle_qty, axis=1)
        df[pc.new_discount] = df.apply(handle_discount, axis=1)
        df[pc.new_discount_money] = df.apply(handle_discount_money, axis=1)
        df[pc.new_fee_count] = df.apply(handle_fee_count, axis=1)
        df[pc.new_fee] = df[fee_column]

        return df

    def _modify_attribute_manager(self, map_df, data_df, attribute_manager):
        attribute_manager.get(pc.map_data).value = \
            pc.new_qty + ":" + pc.new_qty + ":1," \
            + pc.new_money + ":" + pc.new_money + ":1," \
            + pc.new_fee_count + ":" + pc.new_fee_count + ":1," \
            + pc.new_fee + ":" + pc.new_fee + ":1"

    def support(self, pay_type):
        return "绿洲样品" == pay_type

    def _doing_merger_modify(self, map_df_row, data_df, attribute_manager):
        material_name_column, qty_column, price_column, fee_column = list(
            str(attribute_manager.value(pc.map_spec_column)).split(","))
        data_df[pc.new_price] = map_df_row[price_column]

    def _after_merger(self, df_list, attribute_manager):
        if len(df_list) > 0:
            if df_list[0] is not None:
                result_df = df_list[0]
                material_name_column, material_spec_column, qty_column, unit_column, price_column, fee_column = list(
                    str(attribute_manager.value(pc.data_spec_column)).split(","))

                group = result_df.groupby(by=[pc.new_bill_code, material_name_column, unit_column],
                                          as_index=False)
                result_df[pc.new_discount] = np.nan
                for group_key in group.groups.keys():
                    find_df = result_df[(result_df[pc.new_bill_code] == group_key[0])
                                        & (result_df[material_name_column] == group_key[1])
                                        & (result_df[unit_column] == group_key[2])]
                    if len(find_df) > 0:
                        qty = find_df[pc.new_qty].sum()
                        unit = find_df.iloc[0][unit_column]
                        if unit == "双":
                            if qty >= 20:
                                result_df.loc[find_df.index.values[0], pc.new_discount] = "20%"
                            else:
                                result_df.loc[find_df.index.values[0], pc.new_discount] = "100%"
                        elif unit == "YD":
                            if qty <= 5:
                                result_df.loc[find_df.index.values[0], pc.new_discount] = "100%"
                            elif qty > 10:
                                result_df.loc[find_df.index.values[0], pc.new_discount] = "30%"
                            else:
                                result_df.loc[find_df.index.values[0], pc.new_discount] = "50%"
                        else:
                            result_df.loc[find_df.index.values[0], pc.new_discount] = np.nan

                label_list = [pc.new_bill_code, pc.new_money, pc.new_qty, pc.new_fee_count, pc.new_fee]
                result_df.drop(labels=label_list,
                               axis=1,
                               inplace=True,
                               errors="ignore")
