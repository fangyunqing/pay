# @Time    : 22/09/27 9:06
# @Author  : fyq
# @File    : default_reset_index.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.reset_index.reset_index import ResetIndex


class DefaultResetIndex(ResetIndex):

    def reset_index(self, df_list, attribute_manager):
        for df in df_list:
            df.columns = [str(r) for r in range(0, len(df.columns))]
            df.index = range(0, len(df.index))
