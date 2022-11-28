# @Time    : 22/09/27 9:32
# @Author  : fyq
# @File    : reconciliation_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from functools import reduce
from itertools import combinations

from pay.file_parser.map.abstract_reconciliation_file_parser import AbstractReconciliationFileParser
from pay.reset_index.default_reset_index import DefaultResetIndex
from pay.create_describe_4_excel.reconciliation_create_describe_4_excel import ReconciliationCreateDescribe4Excel
from pay.write_excel.default_write_excel import DefaultWriteExcel
import pay.constant as pc
import pandas as pd
from pay.handle_parser.default_handle_parser import DefaultHandleParser
from pay.render.default_render import DefaultRender
import numpy as np
import re


class ReconciliationFileParser(AbstractReconciliationFileParser):
    """
        普通应收对账 通过订单号查询
    """

    def _do_parse_color(self, df, attribute_manager, is_map):

        df[pc.new_color] = ""
        material_name_column = None
        if is_map:
            if hasattr(self, "map_material_name_column"):
                material_name_column = getattr(self, "map_material_name_column")
        else:
            if hasattr(self, "data_material_name_column"):
                material_name_column = getattr(self, "data_material_name_column")

        use_color = attribute_manager.value(pc.use_color)
        if material_name_column and use_color and use_color == "是":
            color_list = []
            color_map = self._color_map()
            for material_name in df[material_name_column]:
                find = False
                if isinstance(material_name, str):
                    for color_key in color_map.keys():
                        for color in color_key:
                            if color in material_name:
                                color_list.append(color_map[color_key])
                                find = True
                                break
                        if find:
                            break
                if not find:
                    color_list.append("")
            df[pc.new_color] = color_list

    def _do_parse_material_name(self, df, attribute_manager, is_map):

        df[pc.new_material_name] = ""
        material_name_column = None
        if is_map:
            if hasattr(self, "map_material_name_column"):
                material_name_column = getattr(self, "map_material_name_column")
        else:
            if hasattr(self, "data_material_name_column"):
                material_name_column = getattr(self, "data_material_name_column")

        mate = attribute_manager.value(pc.mate).strip()
        if material_name_column and len(mate) > 0:
            mate_list = mate.split(",")
            material_name_list = []
            for material_name in df[material_name_column]:
                find = False
                if isinstance(material_name, str):
                    for m in mate_list:
                        pattern = re.compile(m)
                        res = re.search(pattern, material_name.strip().replace(" ", ""))
                        if res:
                            material_name_list.append(res.group().upper())
                            find = True
                            break
                if not find:
                    material_name_list.append(material_name)
            df[pc.new_material_name] = material_name_list

    def _do_parse_spec_column(self, attribute_manager):
        pass

    def _before_merger(self, map_df_info_list, data_df, attribute_manager):
        pass

    def _after_parse_map(self, df, attribute_manager):
        map_bill_code = attribute_manager.value(pc.map_bill_code)
        df[pc.new_bill_code] = df[map_bill_code]
        return [df, [pc.new_bill_code]]

    def _doing_parse_map(self, file_dict, attribute_manager):
        map_file_info = str(attribute_manager.value(pc.map_file)).split(",")
        map_use_column_list = list(attribute_manager.value(pc.map_use_column).split(","))
        map_bill_code = attribute_manager.value(pc.map_bill_code)
        map_df = DefaultHandleParser().handle_parser(file_dict=file_dict,
                                                     file_info=map_file_info,
                                                     use_column_list=map_use_column_list,
                                                     attribute_manager=attribute_manager,
                                                     data_type={int(map_bill_code): str})
        map_df[map_bill_code] = map_df[map_bill_code].apply(lambda x: str(x).strip().replace("'", ""))
        return map_df

    def _after_parse_data(self, df, attribute_manager):
        data_bill_code = attribute_manager.value(pc.data_bill_code)
        df[pc.new_bill_code] = df[data_bill_code]
        return df

    def _doing_parse_data(self, file_dict, attribute_manager):
        data_file_info = str(attribute_manager.value(pc.data_file)).split(",")
        data_use_column_list = list(attribute_manager.value(pc.data_use_column).split(","))
        data_bill_code = attribute_manager.value(pc.data_bill_code)
        data_df = DefaultHandleParser().handle_parser(file_dict=file_dict,
                                                      file_info=data_file_info,
                                                      use_column_list=data_use_column_list,
                                                      attribute_manager=attribute_manager,
                                                      data_type={int(data_bill_code): str})
        data_df[data_bill_code] = data_df[data_bill_code].apply(lambda x: str(x).strip().replace("'", ""))
        return data_df

    def _after_merger(self, df_list, origin_map_df, attribute_manager):
        pass

    @staticmethod
    def _search_data(search_map_df, search_data_df, map_diff, data_diff):

        s_map = search_map_df[map_diff]
        s_data = search_data_df[data_diff]

        for map_times in range(0, len(search_map_df.index)):
            for combination_map_item in combinations(search_map_df.index, map_times + 1):
                map_sum = reduce(lambda x, y: x + y,
                                 [s_map[combination_map_element] for combination_map_element in
                                  combination_map_item])
                for data_times in range(0, len(search_data_df)):
                    for combination_data_item in combinations(search_data_df.index, data_times + 1):
                        data_sum = reduce(lambda x, y: x + y,
                                          [s_data[combination_data_element] for combination_data_element in
                                           combination_data_item])
                        if map_sum == data_sum:
                            return True, list(combination_map_item), list(combination_data_item)

        return False, search_map_df.index.tolist(), search_data_df.index.tolist()

    def _doing_merger(self, map_df_info, data_df, attribute_manager):
        map_df, search_column_list = map_df_info
        self._modify_attribute_manager(map_df, data_df, attribute_manager)
        map_data_list = list(attribute_manager.value(pc.map_data).split(","))
        result_df_list = []
        df_not_found_list = []
        s_total_list = []

        # for map_unique in search_column_list:
        #     map_df[map_unique] = map_df[map_unique].astype("str", errors="ignore").apply(remove_zero)
        #
        # for data_unique in search_column_list:
        #     data_df[data_unique] = data_df[data_unique].astype("str", errors="ignore").apply(remove_zero)

        # 分组查询
        group = map_df.groupby(by=search_column_list, as_index=False)
        for group_key in group.groups.keys():

            # 获取分类的数据
            line = group.groups[group_key]
            if isinstance(group_key, (list, tuple)):
                group_key_list = group_key
            else:
                group_key_list = [group_key]

            if isinstance(line, (list, tuple)):
                line_list = [int(ll[0]) for ll in line]
            else:
                line_list = [int(line[0])]

            search_map_df = map_df.loc[line_list]

            # 查找数据
            search_data_df = data_df
            for search_index, search_column in enumerate(search_column_list):
                search_data_df = search_data_df.loc[search_data_df[search_column] == group_key_list[search_index]]

            # 未找到
            if len(search_data_df.index) == 0:
                df_not_found_list.append(search_map_df)
                continue

            # 删除已经找到的数据
            data_df.drop(labels=search_data_df.index, inplace=True)

            # 钩子处理
            self._doing_merger_modify(map_df_row=search_map_df,
                                      data_df=search_data_df,
                                      attribute_manager=attribute_manager)

            # 统计
            s_total = pd.Series(index=search_column_list)
            s_total_list.append(s_total)
            for search_index, search_column in enumerate(search_column_list):
                s_total.loc[search_column] = group_key_list[search_index]
            # 寻找基点
            map_diff, data_diff, diff_type = map_data_list[0].split(":")
            if diff_type != "1":
                raise Exception("无法寻找到基点")
            find_map_df_list = []
            find_data_df_list = []

            while True:
                find_data, find_map_line_list, find_data_line_list = self._search_data(search_map_df=search_map_df,
                                                                                       search_data_df=search_data_df,
                                                                                       map_diff=map_diff,
                                                                                       data_diff=data_diff)
                find_map_df_list.append(search_map_df.loc[find_map_line_list])
                find_data_df_list.append(search_data_df.loc[find_data_line_list])
                search_map_df.drop(list(find_map_line_list), axis=0, inplace=True, errors="ignore")
                search_data_df.drop(list(find_data_line_list), axis=0, inplace=True, errors="ignore")
                if not find_data or len(search_map_df) == 0:
                    break
            # 校对
            for find_map_df_index, find_map_df in enumerate(find_map_df_list):
                find_data_df = find_data_df_list[find_map_df_index]
                result_df_list.append(find_data_df)
                for map_data_index, map_data in enumerate(map_data_list):
                    map_diff, data_diff, diff_type = map_data.split(":")
                    diff_column = "diff" + str(map_data_index)
                    # 只比较数据
                    if diff_type == "0":
                        find_data_df[diff_column] = np.nan
                        map_unique_list = [round(val, 6) for val in find_map_df[map_diff].unique().tolist()]
                        data_unique_list = [round(val, 6) for val in find_data_df[data_diff].unique().tolist()]
                        s_total.loc[data_diff] = ",".join([str(m) for m in data_unique_list])
                        s_total.loc[map_diff + "-1"] = ",".join([str(m) for m in map_unique_list])
                        for map_unique_index, map_unique in enumerate(map_unique_list):
                            if map_unique != data_unique_list[map_unique_index]:
                                first_row = find_data_df.iloc[0]
                                first_row[diff_column] = ",".join([str(m) for m in map_unique_list])
                                find_data_df.iloc[0] = first_row
                                break
                    else:
                        find_data_df[diff_column] = ""
                        find_data_df[diff_column + "-1"] = ""
                        data_sum = round(find_data_df[data_diff].sum(), 6)
                        map_sum = round(find_map_df[map_diff].sum(), 6)
                        diff = round(map_sum - data_sum, 6)
                        s_total.loc[data_diff] = data_sum
                        s_total.loc[map_diff + "-1"] = map_sum
                        s_total.loc[data_diff + "-" + map_diff] = 0
                        if diff != 0:
                            s_total.loc[data_diff + "-" + map_diff] = diff
                            first_row = find_data_df.iloc[0]
                            first_row[diff_column] = map_sum
                            first_row[diff_column + "-1"] = diff
                            find_data_df.iloc[0] = first_row

        # for ri, r in map_df.iterrows():
        #
        #     df = data_df
        #     for search_column in search_column_list:
        #         df = df.loc[df[search_column] == r[search_column]]
        #
        #     if len(df.index) == 0:
        #         df_not_found_list.append(r.to_frame().T)
        #         continue
        #
        #     # 删除已经找到的数据
        #     data_df.drop(labels=df.index, inplace=True)
        #
        #     self._doing_merger_modify(map_df_row=r,
        #                               data_df=df,
        #                               attribute_manager=attribute_manager)
        #
        #     map_diff_list = []
        #     data_diff_list = []
        #
        #     s_total = pd.Series(index=search_column_list)
        #     s_total_list.append(s_total)
        #     for map_unique in search_column_list:
        #         s_total.loc[map_unique] = r[map_unique]
        #
        #     for i, map_data in enumerate(map_data_list):
        #         map_diff, data_diff, diff_type = map_data.split(":")
        #         map_diff_list.append(map_diff)
        #         data_diff_list.append(data_diff)
        #         diff_column = "diff" + str(i)
        #
        #         if diff_type == "0":
        #             df[diff_column] = ""
        #             s_diff = df[data_diff] == r[map_diff]
        #             s_total.loc[data_diff] = ",".join([str(s) for s in df[data_diff].unique().tolist()])
        #             s_total.loc[map_diff + "-1"] = r[map_diff]
        #             if not s_diff.all():
        #                 first_row = df.iloc[0]
        #                 first_row[diff_column] = r[map_diff]
        #                 df.iloc[0] = first_row
        #         else:
        #             df[diff_column] = ""
        #             df[diff_column + "-1"] = ""
        #             data_sum = round(df[data_diff].sum(), 6)
        #             map_sum = round(r[map_diff], 6)
        #             diff = round(map_sum - data_sum, 6)
        #             s_total.loc[data_diff] = data_sum
        #             s_total.loc[map_diff + "-1"] = map_sum
        #             s_total.loc[data_diff + "-" + map_diff] = 0
        #             if abs(diff) != 0:
        #                 s_total.loc[data_diff + "-" + map_diff] = diff
        #                 first_row = df.iloc[0]
        #                 first_row[diff_column] = map_sum
        #                 first_row[diff_column + "-1"] = diff
        #                 df.iloc[0] = first_row
        #     df_list.append(df)
        df_total = None
        if len(s_total_list) > 0:
            df_total = pd.concat(s_total_list, axis=1, ignore_index=False).T
        df_list = [pd.concat(result_df_list) if len(result_df_list) > 0 else None,
                   pd.concat(df_not_found_list) if len(df_not_found_list) > 0 else None,
                   df_total]
        return df_list

    def _modify_attribute_manager(self, map_df, data_df, attribute_manager):
        pass

    def _do_reset_index(self, df, attribute_manager):
        DefaultResetIndex().reset_index(df, attribute_manager)

    def _do_create_describe_4_excel(self, df, attribute_manager):
        return ReconciliationCreateDescribe4Excel().create_describe_4_excel(df_list=df,
                                                                            attribute_manager=attribute_manager)

    def _do_write_excel(self, describe_excel, attribute_manager, target_file):
        DefaultWriteExcel().write_excel(describe_excel, attribute_manager, target_file)

    def _do_render_target(self, describe_excel_list, attribute_manager, target_file):
        DefaultRender().render(describe_excel_list, attribute_manager, target_file)

    def support(self, pay_type):
        return "常用" == pay_type

    def _doing_merger_modify(self, map_df_row, data_df, attribute_manager):
        pass

    @staticmethod
    def _color_map():
        return {
            ("新螢光深桃紅", "新荧光深桃红"): "新螢光深桃紅",
            ("新螢光火焰紅", "新荧光火焰红"): "新螢光火焰紅",
            ("新暗海藻藍", "新暗海藻蓝"): "新暗海藻藍",
            ("新螢光霓綠", "新荧光霓绿", "新萤光霓绿"): "新螢光霓綠",
            ("新海藻藍", "新海藻蓝"): "新海藻藍",
            ("新紅層灰", "新红层灰"): "新紅層灰",
            ("新深寶藍", "新深宝蓝"): "新深寶藍",
            ("新黃層灰", "新黄层灰"): "新黃層灰",
            ("新墨綠藍", "新墨绿蓝"): "新墨綠藍",
            ("新淺綠灰", "新浅绿灰"): "新淺綠灰",
            ("新夜橄欖", "夜橄榄"): "新夜橄欖",
            ("新淺灰紫", "新浅灰紫", "新灰紫"): "新淺灰紫",
            ("新盧水灰", "新卢水灰"): "新盧水灰",
            ("新深墨藍", "新深墨蓝"): "新深墨藍",
            ("新喜米綠", "新喜米绿"): "新喜米綠",
            ("新優雅粉", "新优雅粉"): "新優雅粉",
            ("新布李紫",): "新布李紫",
            ("新輕盈藍", "新轻盈蓝"): "新輕盈藍",
            ("新棉糖粉",): "新棉糖粉",
            ("新非洲沙",): "新非洲沙",
            ("新褐灰", "新褐"): "新褐灰",
            ("新香粉",): "新香粉",
            ("新軒紅", "新轩红"): "新軒紅",
            ("新巧紫",): "新巧紫",
            ("新銀灰", "新银灰"): "新銀灰",
            ("新水粉",): "新水粉",
            ("新橄欖", "新橄榄"): "新橄欖",
            ("新水紅", "新水红"): "新水紅",
            ("新藍綠", "藍綠"): "新藍綠",
            ("新蜜紅", "新蜜红"): "新蜜紅",
            ("新黑紫",): "新黑紫",
            ("新潤綠", "新润绿"): "新潤綠",
            ("新鳳灰", "新凤灰"): "新鳳灰",
            ("新藍浪", "新蓝浪"): "新藍浪",
            ("新櫻藍", "新樱蓝"): "新櫻藍",
            ("新水粉",): "新水粉",
            ("新紫晶",): "新紫晶",
            ("新紫",): "新紫",
            ("螢光幻彩粉", "荧光幻彩粉"): "螢光幻彩粉",
            ("螢光石竹紅", "荧光石竹红"): "螢光石竹紅",
            ("深雾蓝", "深霧藍", "深雾藍"): "深霧藍",
            ("迷雅綠", "迷雅绿"): "迷雅綠",
            ("浅绿灰", "淺綠灰"): "淺綠灰",
            ("經典紫", "经典紫"): "經典紫",
            ("海藻藍", "海藻蓝"): "海藻藍",
            ("櫻桃紅",): "櫻桃紅",
            ("暗紫紅", "暗紫红"): "暗紫紅",
            ("鑽石白",): "鑽石白",
            ("大氣褐", "大气褐"): "大氣褐",
            ("枯玫紅", "枯玫红"): "枯玫紅",
            ("海水藍", "海水蓝"): "海水藍",
            ("深湖綠", "深湖绿"): "深湖綠",
            ("沉靜藍", "沉静蓝"): "沉靜藍",
            ("淺霧白", "浅雾白"): "淺霧白",
            ("印度褐",): "印度褐",
            ("墨水藍", "墨水蓝"): "墨水藍",
            ("葡萄藍", "葡萄蓝"): "葡萄藍",
            ("醃菜紫", "腌菜紫"): "醃菜紫",
            ("淺藍灰", "浅蓝灰"): "淺藍灰",
            ("果凍橙", "果冻橙"): "果凍橙",
            ("淡薰紫",): "淡薰紫",
            ("淺紫藍", "浅紫蓝"): "淺紫藍",
            ("天使白",): "天使白",
            ("桃子紅", "桃子红"): "桃子紅",
            ("純淨藍", "纯净蓝"): "純淨藍",
            ("甘粉紅", "甘粉红"): "甘粉紅",
            ("螢光綠", "荧光绿"): "螢光綠",
            ("鯊魚灰",): "鯊魚灰",
            ("迷雅綠",): "迷雅绿",
            ("雪狼白",): "雪狼白",
            ("丁香紫",): "丁香紫",
            ("淡雲灰", "淡云灰"): "淡雲灰",
            ("香雪白",): "香雪白",
            ("瀝青黑",): "瀝青黑",
            ("香雪白",): "香雪白",
            ("罌粟灰",): "罌粟灰",
            ("亮灰",): "亮灰",
            ("暮灰",): "暮灰",
            ("岩粉",): "岩粉",
            ("月褐",): "月褐",
            ("茜草",): "茜草",
            ("山褐",): "山褐",
            ("鐵藍", "铁蓝"): "鐵藍",
            ("靈藍", "灵蓝"): "靈藍",
            ("琥藍", "琥蓝"): "琥藍",
            ("礦藍", "矿蓝"): "礦藍",
            ("霧灰", "雾灰"): "霧灰",
            ("深炭",): "深炭",
            ("冰白",): "冰白",
            ("雨灰",): "雨灰",
            ("梅紫",): "梅紫",
            ("霧紫", "雾紫"): "霧紫",
            ("天藍", "天蓝"): "天藍",
            ("米白",): "米白",
            ("統藍", "統蓝"): "統藍",
            ("白",): "白",
            ("黑",): "黑",
            ("灰",): "灰",
        }
