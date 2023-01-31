# @Time    : 22/09/27 9:32
# @Author  : fyq
# @File    : reconciliation_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import operator
from functools import reduce
from itertools import combinations

from pay.entity import SingleExpress, ExpressParam
from pay.file_parser.map.abstract_reconciliation_file_parser import AbstractReconciliationFileParser
from pay.file_parser.map.diff_type import DiffTypeManager
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
        return [[df, [pc.new_bill_code]]]

    def _doing_parse_map(self, file_dict, attribute_manager):
        map_file_info = str(attribute_manager.value(pc.map_file)).split(",")
        map_use_column_list = list(attribute_manager.value(pc.map_use_column).split(","))
        map_bill_code = attribute_manager.value(pc.map_bill_code)
        map_df = DefaultHandleParser().handle_parser(file_dict=file_dict,
                                                     file_info=map_file_info,
                                                     use_column_list=map_use_column_list,
                                                     attribute_manager=attribute_manager,
                                                     data_type={int(map_bill_code): str})
        map_df = map_df[map_df[map_bill_code].notna()]
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
        data_df = data_df[data_df[data_bill_code].notna()]
        data_df[data_bill_code] = data_df[data_bill_code].apply(lambda x: str(x).strip().replace("'", ""))
        return data_df

    def _after_merger(self, df_list, origin_map_df, attribute_manager):
        super(ReconciliationFileParser, self)._after_merger(df_list, origin_map_df, attribute_manager)
        if len(df_list) > 0:
            if df_list[0] is not None:
                label_list = [pc.new_bill_code]
                df_list[0].drop(labels=label_list,
                                axis=1,
                                inplace=True,
                                errors="ignore")

    @staticmethod
    def _search_data(search_map_df, search_data_df, map_diff, data_diff):

        s_map = search_map_df[map_diff]
        s_data = search_data_df[data_diff]

        if len(search_data_df) == 1 or len(search_map_df) == 1:

            return False, search_map_df.index.tolist(), search_data_df.index.tolist()

        for map_times in range(0, len(search_map_df.index)):
            if map_times > 9:
                return False, search_map_df.index.tolist(), search_data_df.index.tolist()
            for combination_map_item in combinations(search_map_df.index, map_times + 1):
                map_sum = reduce(lambda x, y: x + y,
                                 [s_map[combination_map_element] for combination_map_element in
                                  combination_map_item])
                for data_times in range(0, len(search_data_df)):
                    if data_times > 9:
                        return False, search_map_df.index.tolist(), search_data_df.index.tolist()
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

        # 分组查询
        group = map_df.groupby(by=search_column_list, as_index=False)

        # 基点解析
        check_point = attribute_manager.value(pc.check_point)
        point_map_data_split = map_data_list[int(check_point)].split(":")
        if len(point_map_data_split) == 3:
            point_map_diff, point_data_diff, point_diff_type = \
                map_data_list[attribute_manager.value(pc.check_point)].split(":")
        else:
            point_map_diff, point_data_diff, point_diff_type, point_handle_exp = \
                map_data_list[attribute_manager.value(pc.check_point)].split(":")
        if point_diff_type == "0":
            raise Exception("error")

        for group_key in group.groups.keys():

            # 获取分类的数据
            line = group.groups[group_key].values.tolist()
            if isinstance(group_key, (list, tuple)):
                group_key_list = group_key
            else:
                group_key_list = [group_key]

            line_list = [int(ll) for ll in line]

            search_map_df = map_df.loc[line_list].copy()
            # 查找数据
            search_data_df = data_df.copy()
            for search_index, search_column in enumerate(search_column_list):
                search_data_df = search_data_df.loc[search_data_df[search_column] == group_key_list[search_index]]

            # 未找到
            if len(search_data_df.index) == 0:
                df_not_found_list.append(search_map_df)
                continue

            # 钩子处理
            self._doing_merger_modify(map_df_row=search_map_df,
                                      data_df=search_data_df,
                                      attribute_manager=attribute_manager)

            find_map_df_list = []
            find_data_df_list = []

            while True:
                find_data, find_map_line_list, find_data_line_list = self._search_data(search_map_df=search_map_df,
                                                                                       search_data_df=search_data_df,
                                                                                       map_diff=point_map_diff,
                                                                                       data_diff=point_data_diff)

                if len(find_data_line_list) > 0 and len(find_map_line_list) > 0:
                    find_map_df_list.append(search_map_df.loc[find_map_line_list])
                    find_data_df_list.append(search_data_df.loc[find_data_line_list])
                    search_map_df.drop(list(find_map_line_list), axis=0, inplace=True, errors="ignore")
                    search_data_df.drop(list(find_data_line_list), axis=0, inplace=True, errors="ignore")
                    data_df.drop(list(find_data_line_list), axis=0, inplace=True, errors="ignore")
                elif len(find_data_line_list) == 0:
                    df_not_found_list.append(search_map_df.loc[find_map_line_list])
                    break
                else:
                    break

                if not find_data:
                    break

            # 校对
            for find_map_df_index, find_map_df in enumerate(find_map_df_list):

                # 统计
                s_total = pd.Series(index=search_column_list, dtype="object")
                s_total_list.append(s_total)
                for search_index, search_column in enumerate(search_column_list):
                    s_total.loc[search_column] = group_key_list[search_index]

                find_data_df = find_data_df_list[find_map_df_index].copy()
                result_df_list.append(find_data_df)

                # 判断是基点是否相等
                point_map_sum = round(find_map_df[point_map_diff].sum(), 6)
                point_data_sum = round(find_data_df[point_data_diff].sum(), 6)
                point_equal = point_map_sum == point_data_sum

                stat_result_list = []
                for map_data_index, map_data in enumerate(map_data_list):

                    map_data_split = map_data.split(":")
                    handle_exp = None
                    if len(map_data_split) == 3:
                        map_diff, data_diff, diff_type = map_data_split
                    else:
                        map_diff, data_diff, diff_type, handle_exp = map_data_split
                    if handle_exp is not None and point_equal:
                        single_express = SingleExpress(handle_exp)
                        if single_express.param_one >= len(map_data_list) \
                                or single_express.param_two >= len(map_data_list):
                            raise Exception(pc.error_string.map_error_10003)

                        express_param_one = ExpressParam()
                        express_param_two = ExpressParam()
                        express_param_one.index = single_express.param_one
                        express_param_two.index = single_express.param_two
                        express_param_one.value_list = list(map_data_list[express_param_one.index].split(":"))
                        express_param_two.value_list = list(map_data_list[express_param_two.index].split(":"))

                        if len(express_param_one.value_list) > 4 or len(express_param_two.value_list) > 4:
                            raise Exception(pc.error_string.map_error_10002)

                        if express_param_one.value_list[2] == "0" and express_param_two.value_list[2] == "0":
                            raise Exception(pc.error_string.map_error_10001)

                        total = False
                        # 比较one统计数据
                        if express_param_one.value_list[2] == "1":
                            one_data_sum = find_data_df[express_param_one.value_list[1]].sum()
                            one_map_sum = find_map_df[express_param_one.value_list[0]].sum()
                            if one_map_sum != one_data_sum:
                                total = True

                            zero_data_list = [round(val, 6) for val in
                                              find_map_df[express_param_two.value_list[0]].unique().tolist()]
                            zero_map_list = [round(val, 6) for val in
                                             find_data_df[express_param_two.value_list[1]].unique().tolist()]
                            if len(zero_data_list) > 1 or len(zero_map_list) > 1:
                                total = True
                        else:
                            one_data_sum = find_data_df[express_param_two.value_list[1]].sum()
                            one_map_sum = search_map_df[express_param_two.value_list[0]].sum()
                            if one_map_sum != one_data_sum:
                                total = True

                            zero_data_list = [round(val, 6) for val in
                                              find_map_df[express_param_one.value_list[0]].unique().tolist()]
                            zero_map_list = [round(val, 6) for val in
                                             find_data_df[express_param_one.value_list[1]].unique().tolist()]
                            if len(zero_data_list) > 1 or len(zero_map_list) > 1:
                                total = True

                        stat_result_list.append(
                            DiffTypeManager().get_diff_type(diff_type).handle(map_df=find_map_df,
                                                                              data_df=find_data_df,
                                                                              map_diff=map_diff,
                                                                              data_diff=data_diff,
                                                                              diff_column_name="diff" + str(
                                                                                  map_data_index),
                                                                              point_equal=point_equal,
                                                                              single_express=single_express,
                                                                              express_param_one=express_param_one,
                                                                              express_param_two=express_param_two,
                                                                              stat=total,
                                                                              total_s=s_total))
                    else:
                        stat_result_list.append(
                            DiffTypeManager().get_diff_type(diff_type).handle(map_df=find_map_df,
                                                                              data_df=find_data_df,
                                                                              map_diff=map_diff,
                                                                              data_diff=data_diff,
                                                                              diff_column_name="diff" + str(
                                                                                  map_data_index),
                                                                              point_equal=point_equal,
                                                                              single_express=None,
                                                                              express_param_one=None,
                                                                              express_param_two=None,
                                                                              stat=True,
                                                                              total_s=s_total))
                stat_result_list = list(set(
                    [not item for item in filter(lambda item: item is not None, stat_result_list)]))
                if len(find_data_df) > 1 and len(stat_result_list) > 1:
                    for map_data_index, map_data in enumerate(map_data_list):
                        find_column_name = []
                        for column_name in find_data_df.columns:
                            if str(column_name).startswith("diff" + str(map_data_index)):
                                find_column_name.append(column_name)

                        diff_type = map_data.split(":")[2]
                        for column_name in find_column_name:
                            if not find_data_df[column_name].isnull().any():
                                if diff_type == "0":
                                    result_list = find_data_df[column_name].unique().tolist()
                                    find_data_df[column_name] = np.nan
                                    first_s = find_data_df.iloc[0].copy()
                                    first_s[column_name] = ".".join([str(r) for r in result_list])
                                    find_data_df.iloc[0] = first_s
                                elif diff_type == "1":
                                    result_sum = find_data_df[column_name].sum()
                                    find_data_df[column_name] = np.nan
                                    first_s = find_data_df.iloc[0].copy()
                                    first_s[column_name] = result_sum
                                    find_data_df.iloc[0] = first_s

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
