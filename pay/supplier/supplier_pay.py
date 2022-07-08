# @Time    : 22/07/06 8:55
# @Author  : fyq
# @File    : supplier_pay.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.abstract_pay import AbstractPay
import pandas as pd


class SupplierPay(AbstractPay):

    def _sheet_info(self):
        sheet_info_list = super(SupplierPay, self)._sheet_info()
        sheet_name, start_row = self["write_detail_sheet"].split(",")
        sheet_info_list.append((sheet_name, int(start_row)))
        return sheet_info_list

    def _parse(self, df_dict):
        df_list = []
        for key in df_dict.keys():
            df = df_dict[key]
            # dept type supplier 分组合计
            df_group = df.groupby([self.dept_column, self["type_column"], self["supplier_column"]],
                                  as_index=False).sum()
            # 排序
            self.sort(df_group)
            # 加入队列
            df_list.append(df_group)
        # 明细
        df_detail_total = pd.concat(df_list)
        df_top_detail_total = df_detail_total.drop([self.dept_column, self["type_column"], self["supplier_column"]],
                                                   axis=1, errors="ignore").sum().to_frame().T
        df_top_detail_total.insert(column=self["supplier_column"], value="", loc=0)
        df_top_detail_total.insert(column=self["type_column"], value="", loc=0)
        df_top_detail_total.insert(column=self.dept_column, value="", loc=0)
        # 去除dept列
        df_total = df_detail_total.drop([self.dept_column], axis=1, errors="ignore")
        # 根据type和supplier分组合计
        df_total_dict = {}
        df_total_list = []
        df_top_total_list = []
        df_total = df_total.groupby([self["type_column"], self["supplier_column"]], as_index=False).sum()
        for type_name in df_total[self["type_column"]].unique():
            df_type = df_total[df_total[self["type_column"]] == type_name]
            # 根据type分组合计
            df_type_total = df_type.groupby(self["type_column"], as_index=False).sum()
            df_type_total.insert(column=self["supplier_column"], value="", loc=1)
            df_type_total[self["type_column"]] = type_name + "汇总"
            df = pd.concat([df_type_total, df_type])
            # 排序
            self.sort(df)
            df_total_dict[type_name] = df
            df_type_total[self["type_column"]] = type_name
            df_top_total_list.append(df_type_total)
        # 根据supplier分组合计
        df_top_total = pd.concat(df_top_total_list)
        df_top_total[self["supplier_column"]] = "小计"
        df_top_total_total = df_top_total.groupby([self["supplier_column"]], as_index=False).sum()
        df_top_total_total.insert(column=self["type_column"], value="", loc=0)
        df_top_total_total[self["supplier_column"]] = "合计"
        self.sort(df_top_total)
        for type_name in df_top_total[self["type_column"]]:
            if type_name in df_total_dict.keys():
                df_total_list.append(df_total_dict[type_name])
        df_total = pd.concat([df_top_total_total, df_top_total, pd.concat(df_total_list)])
        return [df_total, pd.concat([df_top_detail_total, df_detail_total])]
