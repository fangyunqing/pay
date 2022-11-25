# @Time    : 22/11/18 14:36
# @Author  : fyq
# @File    : green_sample_dye_fee_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'


from pay.file_parser.map import ReconciliationFileParser
import pay.constant as pc


class GreenSampleDyeFeeFileParser(ReconciliationFileParser):
    """
        绿洲样品材料费
    """

    def _after_parse_map(self, df, attribute_manager):
        fee_column, = list(
            str(attribute_manager.value(pc.map_spec_column)).split(","))
        df[fee_column].fillna(0, inplace=True)

        def handle_fee_count(row):
            return 1 if row[fee_column] != 0 else 0

        map_bill_code = attribute_manager.value(pc.map_bill_code)
        df[pc.new_bill_code] = df[map_bill_code]
        df[pc.new_fee_count] = df.apply(handle_fee_count, axis=1)
        df[pc.new_fee] = df[fee_column]

        first_df = df[[pc.new_bill_code, pc.new_fee_count, pc.new_fee]] \
            .groupby(by=[pc.new_bill_code], as_index=False) \
            .sum()

        return [[first_df, [pc.new_bill_code]]]

    def _after_parse_data(self, df, attribute_manager):
        fee_column,  = list(
            str(attribute_manager.value(pc.data_spec_column)).split(","))
        df[fee_column].fillna(0, inplace=True)

        def handle_fee_count(row):
            return 1 if row[fee_column] != 0 else 0

        data_bill_code = attribute_manager.value(pc.data_bill_code)
        df[pc.new_bill_code] = df[data_bill_code]
        df[pc.new_fee_count] = df.apply(handle_fee_count, axis=1)
        df[pc.new_fee] = df[fee_column]

        return df

    def _after_merger(self, df_list, attribute_manager):
        if len(df_list) > 0:
            if df_list[0] is not None:
                label_list = [pc.new_bill_code, pc.new_fee_count, pc.new_fee]
                df_list[0].drop(labels=label_list,
                                axis=1,
                                inplace=True,
                                errors="ignore")

    def _modify_attribute_manager(self, map_df, data_df, attribute_manager):
        attribute_manager.get(pc.map_data).value = \
            pc.new_fee_count + ":" + pc.new_fee_count + ":1," \
            + pc.new_fee + ":" + pc.new_fee + ":1"

    def support(self, pay_type):
        return "绿洲样品-染费" == pay_type


