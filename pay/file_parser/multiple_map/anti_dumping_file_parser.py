# @Time    : 22/11/10 13:11
# @Author  : fyq
# @File    : anti_dumping_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.create_describe_4_excel.default_create_describe_4_excel import DefaultCreateDescribe4Excel
from pay.file_parser.multiple_map.abstract_multiple_map_file_parser import AbstractMultipleMapFileParser
import pandas as pd
import numpy as np

from pay.render.default_render import DefaultRender
from pay.reset_index.default_reset_index import DefaultResetIndex
from pay.write_excel.default_write_excel import DefaultWriteExcel


class AntiDumpingFileParser(AbstractMultipleMapFileParser):

    def __init__(self):
        self.sale_name = ["销售出库列表", 2]
        self.trade_name = ["贸易", 3]
        self.recv_dir_name = ["工厂应收单", 2]
        self.bill_name = ["增值税专普发票数据", 6]
        self.inline_name = ["应收单列表-内部关联方", 3]
        self.path_name = ["路径对应供应商", 1]

    def _do_parse_data(self, file_dict, target_file, attribute_manager):
        sale_df_list = []
        recv_df_list = []
        trade_df_list = []
        bill_df_list = []
        inline_df_list = []
        path_df_list = []
        data_df = None
        for key in file_dict.keys():
            if self.recv_dir_name[0] in key:
                for file_path in file_dict[key]:
                    df_list = pd.read_excel(io=file_path,
                                            sheet_name=None,
                                            skiprows=self.recv_dir_name[1],
                                            header=None)
                    if len(df_list) > 0:
                        recv_df_list.extend([df_list[key] for key in df_list.keys()])
            else:
                df_list = pd.read_excel(io=file_dict[key],
                                        sheet_name=None,
                                        skiprows=2,
                                        header=None)
                if len(df_list) > 0:
                    if self.sale_name[0] in key:
                        df_list = pd.read_excel(io=file_dict[key],
                                                sheet_name=None,
                                                skiprows=self.sale_name[1],
                                                header=None)
                        if len(df_list) > 0:
                            sale_df_list.extend([df_list[key] for key in df_list.keys()])
                    elif self.trade_name[0] in key:
                        df_list = pd.read_excel(io=file_dict[key],
                                                sheet_name=None,
                                                skiprows=self.trade_name[1],
                                                header=None)
                        if len(df_list) > 0:
                            trade_df_list.extend([df_list[key] for key in df_list.keys()])
                    elif self.bill_name[0] in key:
                        df_list = pd.read_excel(io=file_dict[key],
                                                sheet_name=None,
                                                skiprows=self.bill_name[1],
                                                header=None)
                        if len(df_list) > 0:
                            bill_df_list.extend([df_list[key] for key in df_list.keys()])
                    elif self.inline_name[0] in key:
                        df_list = pd.read_excel(io=file_dict[key],
                                                sheet_name=None,
                                                skiprows=self.inline_name[1],
                                                header=None)
                        if len(df_list) > 0:
                            inline_df_list.extend([df_list[key] for key in df_list.keys()])
                    elif self.path_name[0] in key:
                        df_list = pd.read_excel(io=file_dict[key],
                                                sheet_name=None,
                                                skiprows=self.path_name[1],
                                                header=None)
                        if len(df_list) > 0:
                            path_df_list.extend([df_list[key] for key in df_list.keys()])

        df_list = pd.read_excel(io=target_file,
                                sheet_name=None,
                                skiprows=2,
                                header=None)
        if len(df_list) > 0:
            data_df = [df_list[key] for key in df_list.keys()][0]

        for ind, row in data_df.iterrows():
            # 物料编码
            material_code = row[9]
            # 客户编码
            client_code = row[6]
            # 数量
            qty = row[16]

            # 调拨单号
            transfer = row[33]
            if pd.isna(transfer):
                # 销售订单号(32) 物料编码(9) 客户(6) 数量(16)
                # 销售订单号(62) 物料编码(37) 客户(4) 数量(48) => 单据编号(20)
                for sale_df in sale_df_list:
                    df = sale_df[(sale_df[62] == row[32]) & (sale_df[37] == row[9]) & (sale_df[4] == row[6]) & (
                            sale_df[48] == row[16])]
                    if len(df) > 0:
                        transfer = str(df.iloc[0][20])
                        break
            else:
                transfer = str(transfer)

            # 37 - 47 复制为 np.nan
            for index in range(37, 48):
                data_df.loc[ind, index] = np.nan

            # 合同号AL(37) 取F(5)列中包含 NSLMY 开头的字符，字符个数在12-13位，如无此字段则显示空白
            # 发票号AM(38)

            bill_code = str(row[5])
            if bill_code.startswith("NSLMY"):
                split_list = bill_code.split("-")
                data_df.loc[ind, 37] = split_list[0]
                data_df.loc[ind, 38] = split_list[1]
            else:
                # transfer 物料编码(9) 数量(16)
                # 贸易 单据编号(12) 物料编码(25) 数量(36) => 发票号(60)
                # 内联 调拨号(33) 物料编码(9) 数量(16) => 发票号(36)
                for trade_df in trade_df_list:
                    df = trade_df[(trade_df[12] == transfer)
                                  & (trade_df[25] == material_code)
                                  & (trade_df[36] == qty)]
                    if len(df) > 0:
                        data_df.loc[ind, 38] = df.iloc[0][60]
                        break
                if pd.isna(data_df.loc[ind, 38]):
                    for inline_df in inline_df_list:
                        df = inline_df[(inline_df[33] == transfer)
                                       & (inline_df[9] == material_code)
                                       & (inline_df[16] == qty)]
                        if len(df) > 0:
                            data_df.loc[ind, 38] = df.iloc[0][36]
                            break

            # 开票日期(39)
            # 发票号(38)
            # 增值发票 发票号(1) => 开票日期(6)
            for bill_df in bill_df_list:
                df = bill_df[bill_df[1] == data_df.loc[ind, 38]]
                if len(df) > 0:
                    data_df.loc[ind, 39] = df.iloc[0][6]
                    break

            # 仓库(41)
            # transfer 物料编码(9) 客户(6) 数量(16)
            # 单据编号(20) 物料编码(37) 客户(4)  数量(48) => 仓库(26)

            # 备注(40) 仓库(41) == 财务综合仓
            # transfer 物料编码(9) 客户(6) 数量(16)
            # 单据编号(20) 物料编码(37) 客户(4)  数量(48) => 批号(57)

            # 路径(42)
            # transfer 物料编码(9) 客户(6) 数量(16)
            # 单据编号(20) 物料编码(37) 客户(4)  数量(48) => 路径(25)

            # 供应商(43) 路径
            # transfer 物料编码(9) 客户(6) 数量(16)
            # 单据编号(20) 物料编码(37) 客户(4)  数量(48) => 库存组织(2)

            for sale_df in sale_df_list:
                df = sale_df[(sale_df[20] == transfer)
                             & (sale_df[37] == material_code)
                             # & (sale_df[4] == client_code)
                             & (sale_df[48] == qty)]
                if len(df) > 0:
                    data_df.loc[ind, 41] = df.iloc[0][26]
                    if data_df.loc[ind, 41] == "财务综合仓":
                        data_df.loc[ind, 40] = df.iloc[0][57]
                    data_df.loc[ind, 42] = df.iloc[0][25]
                    if data_df.loc[ind, 42] == "无路径":
                        data_df.loc[ind, 43] = df.iloc[0][1]
                    else:
                        for path_df in path_df_list:
                            df = path_df[path_df[0] == data_df.loc[ind, 42]]
                            if len(df) > 0:
                                data_df.loc[ind, 43] = df.iloc[0][1]

                    break

            # 数量(44) 未税金额(45) 发票号(46) 发票日期(47)
            # 调拨单号2(33) 物料编码(9) 客户编码(6) 数量(16) => 16 20 34 35
            for recv_df in recv_df_list:
                df = recv_df[(recv_df[33] == transfer)
                             & (recv_df[9] == material_code)
                             # & (recv_df[6] == client_code)
                             & (recv_df[16] == qty)]
                if len(df) > 0:
                    data_df.loc[ind, 44] = df.iloc[0][16]
                    data_df.loc[ind, 45] = df.iloc[0][20]
                    data_df.loc[ind, 46] = df.iloc[0][34]
                    data_df.loc[ind, 47] = df.iloc[0][35]

        return [data_df]

    def _do_create_describe_4_excel(self, df, attribute_manager):
        return DefaultCreateDescribe4Excel().create_describe_4_excel(df_list=df,
                                                                     attribute_manager=attribute_manager)

    def _do_write_excel(self, describe_excel, attribute_manager, target_file):
        DefaultWriteExcel().write_excel(describe_excel, attribute_manager, target_file)

    def _do_render_target(self, describe_excel_list, attribute_manager, target_file):
        DefaultRender().render(describe_excel_list, attribute_manager, target_file)

    def support(self, pay_type):
        return "反倾销" == pay_type

    def _do_reset_index(self, df, attribute_manager):
        DefaultResetIndex().reset_index(df, attribute_manager)
