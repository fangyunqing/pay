# @Time    : 22/12/17 16:14
# @Author  : fyq
# @File    : diff_type_zero.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.file_parser.map.diff_type.diff_type import DiffType
import numpy as np


class DiffTypeZero(DiffType):

    def handle(self, map_df, data_df,
               map_diff, data_diff, diff_column_name,
               point_equal,
               single_express, express_param_one, express_param_two,
               stat,
               total_s):
        map_unique_list = [round(val, 6) for val in map_df[map_diff].unique().tolist()]
        data_unique_list = [round(val, 6) for val in data_df[data_diff].unique().tolist()]
        data_df[diff_column_name] = np.nan
        if (len(map_unique_list) != 1 or len(data_unique_list) != 1) or (data_unique_list[0] != map_unique_list[0]):
            total_s.loc[data_diff] = ",".join([str(m) for m in data_unique_list])
            total_s.loc[map_diff] = ",".join([str(m) for m in map_unique_list])
            if (point_equal and stat) or (not point_equal):
                if not point_equal:
                    first_s = data_df.iloc[0].copy()
                    first_s[diff_column_name] = ",".join([str(m) for m in map_unique_list])
                    data_df.iloc[0] = first_s
                else:
                    data_df[diff_column_name] = map_unique_list[0]
                return True
            else:
                if express_param_one.value_list[2] == "0":
                    zero_data = map_df[express_param_one.value_list[1]].unique().tolist()[0]
                    one_index = express_param_two.value_list[1]
                else:
                    zero_data = map_df[express_param_two.value_list[1]].unique().tolist()[0]
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
                return False

    def support(self):
        return "0"
