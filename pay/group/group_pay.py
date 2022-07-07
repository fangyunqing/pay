# @Time    : 22/07/06 8:36
# @Author  : fyq
# @File    : group_pay.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.abstract_pay import AbstractPay
import pandas as pd


class GroupPay(AbstractPay):

    def __init__(self, attribute_dict):
        super(GroupPay, self).__init__(attribute_dict)
        self.first_merge = True

    def _parse(self, df_dict):
        for key in df_dict.keys():
            df = df_dict[key]
            # 去除supplier列
            df.drop([self["supplier_column"]], axis=1, inplace=True, errors="ignore")
            # 根据dept和type统计
            df = df.groupby([self.dept_column, self["type_column"]], as_index=False).sum()
            # 根据dept统计
            df_total = df.groupby([self.dept_column], as_index=False).sum()
            df_total.insert(column=self["type_column"], value="合计", loc=1)
            # 替换
            df_dict[key] = pd.concat([df_total, df])
            # 排序
            self.sort(df_dict[key])

        dept_list = list(self["dept"].split(","))
        df_list = []
        tmp_df_dict = {}
        for index, dept in enumerate(dept_list[1:]):
            dept_little = list(dept.split("-"))
            # 大于1 合计项
            if len(dept_little) > 1:
                dept_little_list = []
                for dl in dept_little[1:]:
                    if dl in df_dict.keys():
                        dept_little_list.append(df_dict[dl])
                if len(dept_little_list) > 0:
                    df_little = pd.concat(dept_little_list)
                    df_little = df_little.groupby([self["type_column"]], as_index=False).sum()
                    df_little.insert(column=self.dept_column, value=dept_little[0], loc=0)
                    self.sort(df_little)
                    df_list.append(df_little)
            else:
                if dept in df_dict.keys():
                    df_list.append(df_dict[dept])
                    tmp_df_dict[dept] = df_dict[dept]
        # 总计
        df_group = pd.concat(tmp_df_dict.values()).groupby([self["type_column"]], as_index=False).sum()
        df_group.insert(column=self.dept_column, value=dept_list[0], loc=0)
        self.sort(df_group)
        df_list.insert(0, df_group)

        return [pd.concat(df_list)]
