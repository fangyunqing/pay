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

    def _do_parse_spec_column(self, attribute_manager):
        self.map_material_name_column, self.map_color, self.map_qty, self.map_price, self.map_money = list(
            str(attribute_manager.value(pc.map_spec_column)).split(","))

        self.data_color, self.data_material_name_column, self.data_qty, self.data_price, self.data_money = \
            list(str(attribute_manager.value(pc.data_spec_column)).split(","))

    def _after_parse_map(self, df, attribute_manager):

        map_bill_code = attribute_manager.value(pc.map_bill_code)
        df[pc.new_bill_code] = df[map_bill_code]
        df[pc.new_color] = df[self.map_color]

        first_df = df[[pc.new_bill_code, pc.new_material_name, pc.new_color, self.map_qty, self.map_price,
                       self.map_money]] \
            .groupby(by=[pc.new_bill_code, pc.new_material_name, pc.new_color, self.map_price], as_index=False) \
            .sum()

        def second_df(map_df):
            return map_df[[pc.new_bill_code, pc.new_color, self.map_qty, self.map_price, self.map_money]] \
                .groupby(by=[pc.new_bill_code, pc.new_color, self.map_price], as_index=False) \
                .sum()

        return [[first_df, [pc.new_bill_code, pc.new_material_name, pc.new_color]],
                [second_df, [pc.new_bill_code, pc.new_color]]]

    def _after_parse_data(self, df, attribute_manager):

        data_bill_code = attribute_manager.value(pc.data_bill_code)
        df[pc.new_bill_code] = df[data_bill_code]
        df[pc.new_color] = df[self.data_color]

        return df

    def support(self, pay_type):
        return "特步样品" == pay_type

    def _after_merger(self, df_list, origin_map_df, attribute_manager):
        super(TeBuSampleFileParser, self)._after_merger(df_list, origin_map_df, attribute_manager)
        if len(df_list) > 0:
            if df_list[0] is not None:
                label_list = [pc.new_bill_code, pc.new_material_name, pc.new_color]
                df_list[0].drop(labels=label_list,
                                axis=1,
                                inplace=True,
                                errors="ignore")
