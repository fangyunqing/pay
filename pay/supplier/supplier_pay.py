# @Time    : 22/07/06 8:55
# @Author  : fyq
# @File    : supplier_pay.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.abstract_pay import AbstractPay
import pandas as pd


class SupplierPay(AbstractPay):

    def _write_excel(self, target_file, df_list):
        write_info = super(SupplierPay, self)._write_excel(target_file, df_list)
        with pd.ExcelWriter(target_file, engine='openpyxl', mode='a', if_sheet_exists="overlay") as writer:
            sheet_name, start_row = self["write_detail_sheet"].split(",")
            df_list[1].to_excel(writer,
                                startrow=int(start_row),
                                sheet_name=sheet_name,
                                header=None,
                                index=None)

        write_info.append((len(df_list[1].index), len(df_list[1].columns), int(start_row), target_file, sheet_name))
        return write_info

    def _parse(self, df_list):
        for index, df in enumerate(df_list):
            # dept type supplier 分组合计
            df_list[index] = df.groupby([self.dept_column, self["type_column"], self["supplier_column"]], as_index=False).sum()
        # 明细
        df_detail_total = pd.concat(df_list)
        # 去除dept列
        df_total = df_detail_total.drop([self.dept_column], axis=1, errors="ignore")
        # 根据type和supplier分组合计
        df_total_list = []
        df_top_total_list = []
        df_total = df_total.groupby([self["type_column"], self["supplier_column"]], as_index=False).sum()
        for type_name in df_total[self["type_column"]].unique():
            df_type = df_total[df_total[self["type_column"]] == type_name]
            # 根据type分组合计
            df_type_total = df_type.groupby(self["type_column"], as_index=False).sum()
            df_type_total.insert(column=self["supplier_column"], value="", loc=1)
            df_type_total[self["type_column"]] = type_name + "汇总"
            df_total_list.append(pd.concat([df_type_total, df_type]))
            df_top_total_list.append(df_type_total)
        # 根据supplier分组合计
        df_top_total = pd.concat(df_top_total_list)
        df_top_total[self["supplier_column"]] = "小计"
        df_top_total_total = df_top_total.groupby([self["supplier_column"]], as_index=False).sum()
        df_top_total_total.insert(column=self["type_column"], value="", loc=0)
        df_top_total_total[self["supplier_column"]] = "合计"
        df_total = pd.concat([df_top_total_total, df_top_total, pd.concat(df_total_list)])
        return [df_total, df_detail_total]












