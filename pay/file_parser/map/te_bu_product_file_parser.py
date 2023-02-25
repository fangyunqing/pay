# @Time    : 22/11/15 11:48
# @Author  : fyq
# @File    : te_bu_product_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.file_parser.map import ReconciliationFileParser
import pay.constant as pc
import pandas as pd
from decimal import Decimal
from decimal import ROUND_HALF_UP, ROUND_HALF_EVEN


class TeBuProductFileParser(ReconciliationFileParser):

    def _do_parse_spec_column(self, attribute_manager):
        self.map_material_name_column, self.map_qty, self.map_price, self.map_money = list(
            str(attribute_manager.value(pc.map_spec_column)).split(","))

        self.data_material_name_column, self.data_qty, self.data_price, self.data_money, self.data_rate = \
            list(str(attribute_manager.value(pc.data_spec_column)).split(","))

    def _after_parse_map(self, df, attribute_manager):

        def second_df(map_df):
            return map_df[[pc.new_bill_code, self.map_qty, self.map_price, self.map_money]]\
                .groupby(by=[pc.new_bill_code, self.map_price], as_index=False).sum()

        map_bill_code = attribute_manager.value(pc.map_bill_code)
        df[pc.new_bill_code] = df[map_bill_code]
        first_df = df[[pc.new_bill_code, pc.new_material_name, self.map_qty, self.map_price, self.map_money]] \
            .groupby(by=[pc.new_bill_code, pc.new_material_name, self.map_price], as_index=False) \
            .sum()

        return [(first_df, [pc.new_bill_code, pc.new_material_name]),
                (second_df, [pc.new_bill_code])]

    def _after_parse_data(self, df, attribute_manager):

        def handle_price(row):

            if pd.isna(row[self.data_rate]) or pd.isna(row[self.data_price]):
                return row[self.data_price]

            _rate = str(row[self.data_rate]).strip()
            new_price = row[self.data_price]
            if len(_rate) > 0:
                if _rate.startswith("0."):
                    _rate = float(_rate) + 1
                else:
                    _rate.replace("%", "")
                    _rate = float(_rate) / 100 + 1
                new_price = row[self.data_price] / _rate
            return float(Decimal(str(new_price)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))

        def handle_money(row):
            if pd.isna(row[self.data_qty]) or pd.isna(row[pc.new_price]):
                return row[self.data_money]
            m = round(row[self.data_qty] * row[pc.new_price], 6)
            return float(Decimal(str(m)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))

        data_bill_code = attribute_manager.value(pc.data_bill_code)
        df[pc.new_bill_code] = df[data_bill_code]
        df[pc.new_price] = df.apply(handle_price, axis=1)
        df[pc.new_money] = df.apply(handle_money, axis=1)

        return df

    def support(self, pay_type):
        return "特步量产" == pay_type

    def _after_merger(self, df_list, origin_map_df, attribute_manager):
        super(TeBuProductFileParser, self)._after_merger(df_list, origin_map_df, attribute_manager)

        if len(df_list) > 0:
            if df_list[0] is not None:
                label_list = [pc.new_bill_code, pc.new_material_name]
                df_list[0].drop(labels=label_list,
                                axis=1,
                                inplace=True,
                                errors="ignore")

    def _modify_attribute_manager(self, map_df, data_df, attribute_manager):
        map_data_attribute = attribute_manager.get(pc.map_data)
        new_map_data_value_list = []
        for map_data in map_data_attribute.value.split(","):
            map_data_list = map_data.split(":")
            if map_data_list[1] == self.data_price:
                map_data_list[1] = pc.new_price
            elif map_data_list[1] == self.data_money:
                map_data_list[1] = pc.new_money
            new_map_data_value_list.append(":".join(map_data_list))
        map_data_attribute.value = ",".join(new_map_data_value_list)
