# @Time    : 22/11/15 11:48
# @Author  : fyq
# @File    : te_bu_product_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.file_parser.map import ReconciliationFileParser
import pay.constant as pc
import re
import pandas as pd


class TeBuProductFileParser(ReconciliationFileParser):

    def _after_parse_map(self, df, attribute_manager):
        material_name_column, qty, price, money = list(
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

        def group_by_new_bill_code(map_df):
            return map_df[[pc.new_bill_code, qty, price, money]] \
                .groupby(by=[pc.new_bill_code, price], as_index=False) \
                .sum()

        map_bill_code = attribute_manager.value(pc.map_bill_code)
        df[pc.new_bill_code] = df[map_bill_code]
        df[pc.new_material_name] = df.apply(handle_material_name, axis=1)

        first_df = df[[pc.new_bill_code, pc.new_material_name, qty, price, money]] \
            .groupby(by=[pc.new_bill_code, pc.new_material_name, price], as_index=False) \
            .sum()

        return [(first_df, [pc.new_bill_code, pc.new_material_name]),
                (group_by_new_bill_code, [pc.new_bill_code])]

    def _after_parse_data(self, df, attribute_manager):
        material_name_column, qty, price, money, rate = list(
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

        def handle_price(row):

            if pd.isna(row[rate]) or pd.isna(row[price]):
                return row[price]

            _rate = str(row[rate]).strip()
            new_price = row[price]
            if len(_rate) > 0:
                if _rate.startswith("0."):
                    _rate = float(_rate) + 1
                else:
                    _rate.replace("%", "")
                    _rate = float(_rate) / 100 + 1
                new_price = row[price] / _rate
            return round(new_price, 2)

        def handle_money(row):
            if pd.isna(row[qty]) or pd.isna(row[pc.new_price]):
                return row[money]
            return round(row[qty] * row[pc.new_price], 2)

        data_bill_code = attribute_manager.value(pc.data_bill_code)
        df[pc.new_bill_code] = df[data_bill_code]
        df[pc.new_material_name] = df.apply(handle_material_name, axis=1)
        df[pc.new_price] = df.apply(handle_price, axis=1)
        df[pc.new_money] = df.apply(handle_money, axis=1)

        return df

    def support(self, pay_type):
        return "特步量产" == pay_type

    def _after_merger(self, df_list, attribute_manager):
        if len(df_list) > 0:
            if df_list[0] is not None:
                label_list = [pc.new_bill_code, pc.new_material_name]
                df_list[0].drop(labels=label_list,
                                axis=1,
                                inplace=True,
                                errors="ignore")

    def _modify_attribute_manager(self, map_df, data_df, attribute_manager):
        map_data_attribute = attribute_manager.get(pc.map_data)
        data_material_name_column, data_qty, data_price, data_money, data_rate = list(
            str(attribute_manager.value(pc.data_spec_column)).split(","))
        new_map_data_value_list = []
        for map_data in map_data_attribute.value.split(","):
            map_data_list = map_data.split(":")
            if map_data_list[1] == data_price:
                map_data_list[1] = pc.new_price
            elif map_data_list[1] == data_money:
                map_data_list[1] = pc.new_money
            new_map_data_value_list.append(":".join(map_data_list))
        map_data_attribute.value = ",".join(new_map_data_value_list)
