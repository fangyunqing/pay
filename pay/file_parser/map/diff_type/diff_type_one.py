# @Time    : 22/12/17 16:13
# @Author  : fyq
# @File    : diff_type_one.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.file_parser.map.diff_type.diff_type import DiffType
import numpy as np


class DiffTypeOne(DiffType):

    def support(self):
        return "1"

    def handle(self, map_df, data_df,
               map_diff, data_diff, diff_column_name,
               point_equal,
               single_express, express_param_one, express_param_two,
               stat,
               total_s):
        data_sum = round(data_df[data_diff].sum(), 6)
        map_sum = round(map_df[map_diff].sum(), 6)
        diff = round(map_sum - data_sum, 6)
        total_s.loc[data_diff] = data_sum
        total_s.loc[map_diff] = map_sum
        total_s.loc[data_diff + "-" + map_diff] = diff
        data_df[diff_column_name] = np.nan
        data_df[diff_column_name + "-1"] = np.nan
        if diff != 0:
            if (point_equal and stat) or (not point_equal):
                first_s = data_df.iloc[0].copy()
                first_s[diff_column_name] = map_sum
                first_s[diff_column_name + "-1"] = diff
                data_df.iloc[0] = first_s
                return True
            else:
                if express_param_one.value_list[2] == "0":
                    zero_data = map_df[express_param_one.value_list[0]].unique().tolist()[0]
                    one_index = express_param_two.value_list[1]
                else:
                    zero_data = map_df[express_param_two.value_list[0]].unique().tolist()[0]
                    one_index = express_param_one.value_list[1]

                for data_index, data_row in data_df.iterrows():
                    if express_param_one.value_list[2] == "0":
                        if single_express.is_mul():
                            data_df.loc[data_index, diff_column_name] = zero_data * data_row[one_index]
                        elif single_express.is_sub():
                            data_df.loc[data_index, diff_column_name] = zero_data - data_row[one_index]
                        elif single_express.is_add():
                            data_df.loc[data_index, diff_column_name] = zero_data + data_row[one_index]
                        else:
                            data_df.loc[data_index, diff_column_name] = zero_data / data_row[one_index]
                    else:
                        if single_express.is_mul():
                            data_df.loc[data_index, diff_column_name] = data_row[one_index] * zero_data
                        elif single_express.is_sub():
                            data_df.loc[data_index, diff_column_name] = data_row[one_index] - zero_data
                        elif single_express.is_add():
                            data_df.loc[data_index, diff_column_name] = data_row[one_index] + zero_data
                        else:
                            data_df.loc[data_index, diff_column_name] = data_row[one_index] / zero_data
                    data_df.loc[data_index, diff_column_name + "-1"] = \
                        round(data_df.loc[data_index, diff_column_name] - data_row[data_diff], 6)
                return False
