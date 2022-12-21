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

    def _do_parse_spec_column(self, attribute_manager):
        self.map_material_name_column, self.map_qty_column, self.map_price_column, self.map_fee_column = list(
            str(attribute_manager.value(pc.map_spec_column)).split(","))

        self.data_material_name_column, self.data_material_spec_column, self.data_qty_column, self.data_unit_column, \
            self.data_price_column, self.data_fee_column = \
            list(str(attribute_manager.value(pc.data_spec_column)).split(","))

    def _after_parse_map(self, df, attribute_manager):
        df[self.map_fee_column].fillna(0, inplace=True)
        df[self.map_price_column].fillna(0, inplace=True)
        df[self.map_qty_column].fillna(0, inplace=True)
        df[self.map_material_name_column].fillna("", inplace=True)

        def handle_fee_count(row):
            return 1 if row[self.map_fee_column] != 0 else 0

        def handle_qty(row):
            if row[self.map_price_column] == 0:
                return 0
            else:
                return row[self.map_qty_column]

        def handle_money(row):
            return row[self.map_price_column] * row[self.map_qty_column]

        map_bill_code = attribute_manager.value(pc.map_bill_code)
        df[pc.new_bill_code] = df[map_bill_code]
        df[pc.new_fee_count] = df.apply(handle_fee_count, axis=1)
        df[pc.new_fee] = df[self.map_fee_column]
        df[pc.new_money] = df.apply(handle_money, axis=1)
        df[pc.new_qty] = df.apply(handle_qty, axis=1)

        first_df = df[[pc.new_bill_code, pc.new_material_name, pc.new_color, pc.new_money, pc.new_qty,
                       self.map_price_column, pc.new_fee_count, pc.new_fee]] \
            .groupby(by=[pc.new_bill_code, pc.new_material_name, pc.new_color, self.map_price_column], as_index=False) \
            .sum()

        def second_df(map_df):
            return map_df[[pc.new_bill_code, pc.new_color, pc.new_money, pc.new_qty,
                           self.map_price_column, pc.new_fee_count, pc.new_fee]] \
                .groupby(by=[pc.new_bill_code, pc.new_color, self.map_price_column],
                         as_index=False) \
                .sum()

        return [[first_df, [pc.new_bill_code, pc.new_material_name, pc.new_color]],
                [second_df, [pc.new_bill_code, pc.new_color]]]

    def _after_parse_data(self, df, attribute_manager):
        df[self.data_price_column].fillna(0, inplace=True)
        df[self.data_qty_column].fillna(0, inplace=True)
        df[self.data_material_name_column].fillna("", inplace=True)
        df[self.data_material_spec_column].fillna("", inplace=True)
        df[self.data_fee_column].fillna(0, inplace=True)

        def handle_fee_count(row):
            return 1 if row[self.data_fee_column] != 0 else 0

        def handle_qty(row):
            if row[self.data_price_column] == 0:
                return 0
            else:
                return row[self.data_qty_column]

        def handle_money(row):
            return row[self.data_price_column] * row[self.data_qty_column]

        data_bill_code = attribute_manager.value(pc.data_bill_code)
        df[pc.new_bill_code] = df[data_bill_code]
        df[pc.new_money] = df.apply(handle_money, axis=1)
        df[pc.new_qty] = df.apply(handle_qty, axis=1)
        df[pc.new_discount] = np.nan
        df[pc.new_discount_money] = np.nan
        df[pc.new_fee_count] = df.apply(handle_fee_count, axis=1)
        df[pc.new_fee] = df[self.data_fee_column]

        return df

    def _modify_attribute_manager(self, map_df, data_df, attribute_manager):
        attribute_manager.get(pc.map_data).value = \
            pc.new_qty + ":" + pc.new_qty + ":1," \
            + self.map_price_column + ":" + self.data_price_column + ":0," \
            + pc.new_money + ":" + pc.new_money + ":1," \
            + pc.new_fee_count + ":" + pc.new_fee_count + ":1," \
            + pc.new_fee + ":" + pc.new_fee + ":1"

    def support(self, pay_type):
        return "绿洲样品" == pay_type

    def _doing_merger_modify(self, map_df_row, data_df, attribute_manager):
        pass

    def _after_merger(self, df_list, origin_map_df, attribute_manager):
        if len(df_list) > 0:
            if df_list[0] is not None:
                result_df = df_list[0]
                group = result_df.groupby(by=[pc.new_bill_code, self.data_material_name_column, self.data_unit_column],
                                          as_index=False)
                result_df[pc.new_discount] = np.nan
                for group_key in group.groups.keys():
                    find_df = result_df[(result_df[pc.new_bill_code] == group_key[0])
                                        & (result_df[self.data_material_name_column] == group_key[1])
                                        & (result_df[self.data_unit_column] == group_key[2])]
                    if len(find_df) > 0:
                        qty = find_df[pc.new_qty].sum()
                        money = find_df[pc.new_money].sum()
                        unit = find_df.iloc[0][self.data_unit_column]
                        if unit == "双":
                            if qty >= 20:
                                result_df.loc[find_df.index.values[0], pc.new_discount] = "20%"
                                result_df.loc[find_df.index.values[0], pc.new_discount_money] = \
                                    round(0.2 * money, 2)
                            else:
                                result_df.loc[find_df.index.values[0], pc.new_discount] = "100%"
                                result_df.loc[find_df.index.values[0], pc.new_discount_money] = \
                                    round(money, 2)
                        elif unit == "YD":
                            if qty <= 5:
                                result_df.loc[find_df.index.values[0], pc.new_discount] = "100%"
                                result_df.loc[find_df.index.values[0], pc.new_discount_money] = \
                                    round(money, 2)
                            elif qty > 10:
                                result_df.loc[find_df.index.values[0], pc.new_discount] = "30%"
                                result_df.loc[find_df.index.values[0], pc.new_discount_money] = \
                                    round(0.3 * money, 2)
                            else:
                                result_df.loc[find_df.index.values[0], pc.new_discount] = "50%"
                                result_df.loc[find_df.index.values[0], pc.new_discount_money] = \
                                    round(0.5 * money, 2)
                        else:
                            result_df.loc[find_df.index.values[0], pc.new_discount] = np.nan

                label_list = [pc.new_bill_code, pc.new_money, pc.new_qty, pc.new_fee_count, pc.new_fee]
                result_df.drop(labels=label_list,
                               axis=1,
                               inplace=True,
                               errors="ignore")
        super(GreenSampleFeeFileParser, self)._after_merger(df_list, origin_map_df, attribute_manager)
