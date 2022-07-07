# @Time    : 22/07/06 8:36
# @Author  : fyq
# @File    : group_pay.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.abstract_pay import AbstractPay
import pandas as pd


class GroupPay(AbstractPay):

    def _parse(self, df_list):
        for index, df in enumerate(df_list):
            # 去除supplier列
            df.drop([self["supplier_column"]], axis=1, inplace=True, errors="ignore")
            # 根据dept和type统计
            df = df.groupby([self.dept_column, self["type_column"]], as_index=False).sum()
            # 根据dept统计
            df_total = df.groupby([self.dept_column], as_index=False).sum()
            df_total.insert(column=self["type_column"], value="合计", loc=1)
            # 替换
            df_list[index] = pd.concat([df_total, df])

        return [pd.concat(df_list)]
