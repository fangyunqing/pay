# @Time    : 22/11/14 14:30
# @Author  : fyq
# @File    : green_sample_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.file_parser.map import ReconciliationFileParser
import pay.constant as pc
import re


class GreenSampleFileParser(ReconciliationFileParser):

    NEW_MATERIAL_NAME = "new_material_name"
    NEW_MONEY = "new_money"
    NEW_QTY = "new_qty_name"
    NEW_FEE_COUNT = "new_fee_count"
    NEW_FEE = "new_fee"

    def _after_parse_map(self, df, attribute_manager):
        material_name_column, qty_column, price_column, fee_column = list(
            str(attribute_manager.value(pc.map_spec_column)).split(","))
        df[price_column].fillna(0, inplace=True)
        df[qty_column].fillna(0, inplace=True)
        df[fee_column].fillna(0, inplace=True)
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

        # 物料名称的处理
        df[self.NEW_MATERIAL_NAME] = df[material_name_column].apply(handle_material_name)
        df[self.NEW_MONEY] = df.apply(handle_money, axis=1)
        df[self.NEW_QTY] = df.apply(handle_qty, axis=1)
        df[self.NEW_FEE] = df[fee_column]
        df[self.NEW_FEE_COUNT] = df[fee_column].apply(lambda val: 1 if val != 0 else 0)

        map_bill_code = attribute_manager.value(pc.map_bill_code)
        return df[
            [map_bill_code, self.NEW_MATERIAL_NAME, self.NEW_QTY, self.NEW_MONEY, self.NEW_FEE_COUNT, self.NEW_FEE]] \
            .groupby(by=[map_bill_code, self.NEW_MATERIAL_NAME], as_index=False) \
            .sum()

    def _after_parse_data(self, df, attribute_manager):
        material_name_column, material_spec_column, qty_column, price_column, fee_column = list(
            str(attribute_manager.value(pc.data_spec_column)).split(","))
        df[price_column].fillna(0, inplace=True)
        df[qty_column].fillna(0, inplace=True)
        df[fee_column].fillna(0, inplace=True)
        df[material_name_column].fillna("", inplace=True)
        df[material_spec_column].fillna("", inplace=True)

        def handle_material_name(row):
            pattern = re.compile(r"(\d{3}[Gg])")
            res = re.search(pattern, row[material_name_column])
            if res:
                return res.group().upper()
            else:
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

        # 物料名称的处理
        df[self.NEW_MATERIAL_NAME] = df.apply(handle_material_name, axis=1)
        df[self.NEW_MONEY] = df.apply(handle_money, axis=1)
        df[self.NEW_QTY] = df.apply(handle_qty, axis=1)
        df[self.NEW_FEE] = df[fee_column]
        df[self.NEW_FEE_COUNT] = df[fee_column].apply(lambda val: 1 if val != 0 else 0)
        return df

    def _after_merger(self, df_list, attribute_manager):
        if len(df_list) > 0:
            if df_list[0] is not None:
                label_list = [self.NEW_MATERIAL_NAME, self.NEW_MONEY, self.NEW_QTY, self.NEW_FEE, self.NEW_FEE_COUNT]
                df_list[0].drop(labels=label_list,
                                axis=1,
                                inplace=True,
                                errors="ignore")

    def _modify_attribute_manager(self, map_df, data_df, attribute_manager):
        attribute_manager.get(pc.map_data).value = \
            self.NEW_QTY + ":" + self.NEW_QTY + ":1," \
            + self.NEW_MONEY + ":" + self.NEW_MONEY + ":1," \
            + self.NEW_FEE_COUNT + ":" + self.NEW_FEE_COUNT + ":1," \
            + self.NEW_FEE + ":" + self.NEW_FEE + ":1"

    def support(self, pay_type):
        return "绿洲样品" == pay_type

    def _map_unique_column(self, map_bill_code):
        return [map_bill_code, self.NEW_MATERIAL_NAME]

    def _data_unique_column(self, data_bill_code):
        return [data_bill_code, self.NEW_MATERIAL_NAME]
