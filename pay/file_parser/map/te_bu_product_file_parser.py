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
    NEW_MATERIAL_NAME = "new_material_name"
    NEW_PRICE = "new_price"

    def _after_parse_map(self, df, attribute_manager):
        material_name_column, qty = list(
            str(attribute_manager.value(pc.map_spec_column)).split(","))

        def handle_material_name(row):

            if pd.isna(row[material_name_column]):
                return row[material_name_column]

            pattern = re.compile(r"(HF[a-zA-Z\d\-\s]+)")
            res = re.search(pattern, row[material_name_column])
            if res:
                return res.group().upper()
            else:
                return row[material_name_column]

        df[self.NEW_MATERIAL_NAME] = df.apply(handle_material_name, axis=1)

        return df

    def _after_parse_data(self, df, attribute_manager):
        material_name_column, qty, price, rate = list(
            str(attribute_manager.value(pc.data_spec_column)).split(","))

        def handle_material_name(row):

            if pd.isna(row[material_name_column]):
                return row[material_name_column]

            pattern = re.compile(r"(HF[a-zA-Z\d\-\s]+)")
            res = re.search(pattern, row[material_name_column])
            if res:
                return res.group().upper()
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

        df[self.NEW_MATERIAL_NAME] = df.apply(handle_material_name, axis=1)
        df[self.NEW_PRICE] = df.apply(handle_price, axis=1)

        return df

    def support(self, pay_type):
        return "特步量产" == pay_type

    def _after_merger(self, df_list, attribute_manager):
        if len(df_list) > 0:
            if df_list[0] is not None:
                label_list = [self.NEW_MATERIAL_NAME, self.NEW_PRICE]
                df_list[0].drop(labels=label_list,
                                axis=1,
                                inplace=True,
                                errors="ignore")

    def _map_unique_column(self, map_bill_code):
        return [map_bill_code, self.NEW_MATERIAL_NAME]

    def _data_unique_column(self, data_bill_code):
        return [data_bill_code, self.NEW_MATERIAL_NAME]

    def _modify_attribute_manager(self, map_df, data_df, attribute_manager):
        map_data_attribute = attribute_manager.get(pc.map_data)
        price = list(
            str(attribute_manager.value(pc.data_spec_column)).split(","))[2]
        new_map_data_value_list = []
        for map_data in map_data_attribute.value.split(","):
            map_data_list = map_data.split(":")
            if map_data_list[1] == price:
                map_data_list[1] = self.NEW_PRICE
            new_map_data_value_list.append(":".join(map_data_list))
        map_data_attribute.value = ",".join(new_map_data_value_list)

    def _search(self, map_row, data_df, attribute_manager):
        map_bill_code = attribute_manager.value(pc.map_bill_code)
        data_bill_code = attribute_manager.value(pc.data_bill_code)
        map_unique_column = self._map_unique_column(map_bill_code)
        map_unique_column.append(list(
            str(attribute_manager.value(pc.map_spec_column)).split(","))[1])
        data_unique_column = self._data_unique_column(data_bill_code)
        data_unique_column.append(list(
            str(attribute_manager.value(pc.data_spec_column)).split(","))[1])

        # 订单+品名+数量匹配
        df = data_df
        for map_unique_i, map_unique in enumerate(map_unique_column):
            df = df.loc[df[data_unique_column[map_unique_i]] == map_row[map_unique]]

        # 若取不到则不取，直接按订单+数量匹配即可
        map_unique_column.pop(1)
        data_unique_column.pop(1)
        df = data_df
        for map_unique_i, map_unique in enumerate(map_unique_column):
            df = df.loc[df[data_unique_column[map_unique_i]] == map_row[map_unique]]
        return df
