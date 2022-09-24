# @Time    : 22/08/26 16:09
# @Author  : fyq
# @File    : ar_day_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import calendar
import datetime

import pythoncom

from pay.decorator.pay_log import PayLog
from pay.file_parser.abstract_default_file_parser import AbstractDefaultFileParser
import pay.constant as pc
import pandas as pd
import xlwings as xl
from decimal import Decimal


class ARDayFileParser(AbstractDefaultFileParser):

    def _do_parse_df_dict(self, df_dict, attribute_manager):
        # 用户对照
        client_map = str(attribute_manager.value(pc.client_map))
        # 应收出纳数据
        ar_day_data = str(attribute_manager.value(pc.ar_day_data))

        df_client_map = None
        df_ar_day_data = None
        for key in df_dict.keys():
            if client_map.startswith(key):
                df_client_map = df_dict[key]
            elif ar_day_data.startswith(key):
                df_ar_day_data = df_dict[key]

        if df_client_map is None:
            raise Exception("无法找用户对照表,请检查是否配置")
        if df_ar_day_data is None:
            raise Exception("无法找数据表,请检查是否配置")

        ar_begin_date = str(attribute_manager.value(pc.ar_begin_date))
        ar_end_date = str(attribute_manager.value(pc.ar_end_date))
        pay_date_column = str(attribute_manager.value(pc.pay_date))
        df_ar_day_data.dropna(inplace=True)
        df_ar_day_data[pay_date_column] = pd.to_datetime(df_ar_day_data[pay_date_column], format="%Y-%m-%d")
        df_ar_day_data.drop(df_ar_day_data[~((df_ar_day_data[pay_date_column] >= ar_begin_date)
                                             & (df_ar_day_data[pay_date_column] <= ar_end_date))].index,
                            inplace=True)
        water_bill_code = str(attribute_manager.value(pc.water_bill_code))
        map_water_bill_code = str(attribute_manager.value(pc.map_water_bill_code))
        map_bill_code = str(attribute_manager.value(pc.map_bill_code))
        map_client_name_column = str(attribute_manager.value(pc.map_client_name))
        currency_column = str(attribute_manager.value(pc.currency))
        ar_money_column = str(attribute_manager.value(pc.ar_money))
        # 遍历数据行
        df_ar_day_data[pc.bill_code] = ""
        df_ar_day_data[pc.pay_client_name] = ""
        for row_index, row in df_ar_day_data.iterrows():
            df_bill_code = df_client_map[df_client_map[map_water_bill_code] == row[water_bill_code]]
            bill_code_list = []
            map_client_name_list = []
            for value in df_bill_code[map_bill_code]:
                bill_code_list.append(value)
            for value in df_bill_code[map_client_name_column]:
                map_client_name_list.append(value)
            bill_code_list = list(set(bill_code_list))
            df_ar_day_data.loc[row_index, pc.bill_code] = ",".join(bill_code_list)
            df_ar_day_data.loc[row_index, pc.pay_client_name] = ",".join(map_client_name_list)
        df_ar_day_data[currency_column] = df_ar_day_data[currency_column]. \
            apply(lambda val: "人民币" if val.strip() == "RMB" else "美元")
        df_ar_day_data[ar_money_column] = df_ar_day_data[ar_money_column]. \
            apply(lambda x: float(x) / 10000)
        return [df_ar_day_data]

    def _group_column(self, attribute_manager):
        pass

    def support(self, pay_type):
        return True

    def _parser_file(self, key, file, attribute_manager):
        # 用户对照
        client_map = str(attribute_manager.value(pc.client_map))
        # 应收出纳数据
        ar_day_data = str(attribute_manager.value(pc.ar_day_data))

        df = None
        info = None
        use_column = None
        if client_map.startswith(key):
            info = client_map.split(",")
            use_column = self._map_use_column(attribute_manager)
        elif ar_day_data.startswith(key):
            info = ar_day_data.split(",")
            use_column = self._data_use_column(attribute_manager)

        if info is None:
            return None

        df_read_dict = pd.read_excel(io=file,
                                     sheet_name=None,
                                     skiprows=int(info[2]),
                                     header=None,
                                     dtype=str)
        for sheet_name in df_read_dict.keys():
            if sheet_name.strip() == info[1].strip():
                df = df_read_dict[sheet_name]
                break

        if df is None:
            raise Exception("[%s]中无法找工作簿[%s]" % (file, info[1]))

        df.columns = [str(column) for column in df.columns]
        useless_column = []
        for value in df.columns:
            if value not in use_column:
                useless_column.append(value)
        # 去除无用的列
        if len(useless_column) > 0:
            df.drop(useless_column, axis=1, inplace=True, errors="ignore")
        # 删除nan
        df.dropna(how="all")

        return df

    @classmethod
    def _map_use_column(cls, attribute_manager):
        return attribute_manager.value(pc.map_water_bill_code), \
               attribute_manager.value(pc.map_bill_code), \
               attribute_manager.value(pc.map_client_name)

    @classmethod
    def _data_use_column(cls, attribute_manager):
        return attribute_manager.value(pc.water_bill_code), \
               attribute_manager.value(pc.pay_date), \
               attribute_manager.value(pc.ar_money), \
               attribute_manager.value(pc.currency), \
               attribute_manager.value(pc.water_client_name)

    @PayLog(node="渲染excel")
    def _render_target(self, describe_excel_list, attribute_manager, target_file):
        pythoncom.CoInitialize()
        app = xl.App(visible=False, add_book=False)
        try:
            for describe_excel in describe_excel_list:
                df_read_dict = pd.read_excel(io=target_file,
                                             sheet_name=None,
                                             skiprows=describe_excel.start_row,
                                             header=None,
                                             dtype=str)
                df = None
                for sheet_name in df_read_dict.keys():
                    if sheet_name.strip() == describe_excel.sheet_name.strip():
                        describe_excel.sheet_name = sheet_name
                        df = df_read_dict[sheet_name]
                        break

                if df is None:
                    break

                df.columns = [str(column) for column in df.columns]
                df.fillna('0', inplace=True)
                wb = app.books.open(target_file)
                try:
                    sheet = wb.sheets[describe_excel.sheet_name]
                    target_bill_code_column = str(attribute_manager.value(pc.bill_code))
                    target_pay_client_name_column = str(attribute_manager.value(pc.pay_client_name))
                    target_begin_date_column = str(attribute_manager.value(pc.begin_date))
                    pay_date_column = str(attribute_manager.value(pc.pay_date))
                    ar_money_column = str(attribute_manager.value(pc.ar_money))
                    pay_currency_column = str(attribute_manager.value(pc.pay_currency))
                    currency_column = str(attribute_manager.value(pc.currency))
                    water_bill_code_column = str(attribute_manager.value(pc.water_bill_code))
                    water_client_name_column = str(attribute_manager.value(pc.water_client_name))
                    tract_column = str(attribute_manager.value(pc.tract))

                    r_column, r_i_column, n_r_column = list(str(attribute_manager.value(pc.pay_recv)).split(","))

                    ar_begin_date_list = str(attribute_manager.value(pc.ar_begin_date)).split("-")[:2]
                    days = calendar.monthrange(int(ar_begin_date_list[0]), int(ar_begin_date_list[1]))[1]
                    day_end = int(target_begin_date_column) + days - 1
                    df[r_column] = df[r_column].astype(float)
                    df[r_i_column] = df[r_i_column].astype(float)
                    df[n_r_column] = df[n_r_column].astype(float)

                    day_list = []
                    for date in describe_excel.df[pay_date_column].unique():
                        day_list.append(pd.to_datetime(date).day + int(target_begin_date_column) - 1)
                    for c in range(int(target_begin_date_column), day_end + 1):
                        if c in day_list:
                            df[str(c)] = 0
                        df[str(c)] = df[str(c)].astype(float)

                    df_insert_list = []
                    for row_index, row in describe_excel.df.iterrows():
                        if len(row[pc.bill_code]) > 0:
                            df_bill_code = df[df[target_bill_code_column].isin(row[pc.bill_code].split(","))]
                            df_day = row[pay_date_column].day
                            location_day = str(int(target_begin_date_column) + int(df_day) - 1)
                            if len(df_bill_code) > 0:
                                df_bill_code.sort_values(n_r_column, ascending=False, inplace=True)
                                ar_money = row[ar_money_column]
                                for t_index, t_r in df_bill_code.iterrows():
                                    if ar_money == 0:
                                        break
                                    tract_list = []
                                    if t_r[n_r_column] <= 0:
                                        df.loc[t_index, location_day] = \
                                            df_bill_code.loc[t_index, location_day] + ar_money
                                        df_bill_code.loc[t_index, location_day] = \
                                            df_bill_code.loc[t_index, location_day] + ar_money
                                        ar_money = 0
                                        tract_list.append(t_r[location_day])
                                        tract_list.append(str(ar_money) + "(全部金额)")
                                    elif ar_money > t_r[n_r_column]:
                                        df.loc[t_index, location_day] = \
                                            df_bill_code.loc[t_index, location_day]\
                                            + df_bill_code.loc[t_index, n_r_column]
                                        df_bill_code.loc[t_index, location_day] = \
                                            df_bill_code.loc[t_index, location_day] + t_r[n_r_column]
                                        df.loc[t_index, r_i_column] = \
                                            df_bill_code.loc[t_index, r_i_column] \
                                            + df_bill_code.loc[t_index, n_r_column]
                                        df_bill_code.loc[t_index, r_i_column] =  \
                                            df_bill_code.loc[t_index, r_i_column] \
                                            + df_bill_code.loc[t_index, n_r_column]
                                        df.loc[t_index, n_r_column] = 0
                                        ar_money = ar_money - df_bill_code.loc[t_index, n_r_column]
                                        df_bill_code.loc[t_index, n_r_column] = 0
                                        tract_list.append(t_r[location_day])
                                        tract_list.append(str(t_r[n_r_column]) + "(未收)")
                                    else:
                                        df.loc[t_index, location_day] = \
                                            df_bill_code.loc[t_index, location_day] + ar_money
                                        df_bill_code.loc[t_index, location_day] = \
                                            df_bill_code.loc[t_index, location_day] + ar_money
                                        df.loc[t_index, r_i_column] = df_bill_code.loc[t_index, r_i_column] + ar_money
                                        df_bill_code.loc[t_index, r_i_column] = \
                                            df_bill_code.loc[t_index, r_i_column] + ar_money
                                        df.loc[t_index, n_r_column] = \
                                            df_bill_code.loc[t_index, n_r_column] - ar_money
                                        df_bill_code.loc[t_index, n_r_column] = \
                                            df_bill_code.loc[t_index, n_r_column] - ar_money
                                        ar_money = 0
                                        tract_list.append(t_r[location_day])
                                        tract_list.append(str(ar_money) + "(全部金额)")

                                if ar_money > 0:
                                    for t_index, t_r in df_bill_code.iterrows():
                                        df.loc[t_index, location_day] = \
                                            df_bill_code.loc[t_index, location_day] + ar_money
                                        df_bill_code.loc[t_index, location_day] = \
                                            df_bill_code.loc[t_index, location_day] + ar_money
                                        df.loc[t_index, r_i_column] = \
                                            df_bill_code.loc[t_index, r_i_column] + ar_money
                                        df_bill_code.loc[t_index, r_i_column] = \
                                            df_bill_code.loc[t_index, r_i_column] + ar_money
                                        df.loc[t_index, n_r_column] = \
                                            df_bill_code.loc[t_index, n_r_column] - ar_money
                                        df_bill_code.loc[t_index, n_r_column] = \
                                            df_bill_code.loc[t_index, n_r_column] - ar_money
                                        break
                            else:
                                df_insert_list.append(row)
                        else:
                            df_insert_list.append(row)

                    sheet.range((describe_excel.start_row + 1, int(target_begin_date_column) + 1)).value = \
                        df.loc[:, target_begin_date_column: str(day_end)].values

                    if len(df_insert_list) > 0:
                        df_empty = df[(df[target_bill_code_column] == "0")
                                      & (df[pay_currency_column] == "0")]
                        if len(df_empty) == 0:
                            raise Exception("模板[%s]没有充足的行" % target_file)
                        for i_i, df_insert in enumerate(df_insert_list):
                            df_day = df_insert[pay_date_column].day
                            location_day = str(int(target_begin_date_column) + int(df_day) - 1)
                            for e_i, iter_row in enumerate(df_empty.iterrows()):
                                if i_i == e_i:
                                    df.loc[iter_row[0], pay_currency_column] = df_insert[currency_column]
                                    df.loc[iter_row[0], location_day] = df_insert[ar_money_column]
                                    df.loc[iter_row[0], target_bill_code_column] = \
                                        df_insert[water_bill_code_column]
                                    df.loc[iter_row[0], target_pay_client_name_column] \
                                        = df_insert[water_client_name_column].strip()
                                    sheet.range((describe_excel.start_row + 1 + iter_row[0], 1)).value = \
                                        df.loc[iter_row[0]].values
                                    break

                finally:
                    wb.save()
                    wb.close()

        finally:
            app.quit()
            app.kill()
            pythoncom.CoUninitialize()

    def _write_excel(self, describe_excel_list, attribute_manager, target_file):
        pass

    def _reset_index(self, df_parse_list, attribute_manager):
        pass
