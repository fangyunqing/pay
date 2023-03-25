# @Time    : 22/11/09 11:28
# @Author  : fyq
# @File    : wei_lin_pdf_handle_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from typing import List, Any

import pandas
import pdfplumber
from loguru import logger

from pay.handle_parser.handle_parser import HandleParser
from util import format_date, re_startswith
import pay.constant as pc


class WeiLinPdfHandleParser(HandleParser):

    @staticmethod
    def _new_line(df, line_list, line_info: List[Any], start_word, bill_code_prefix, across_column, unit):
        material_list = []
        for index, l_t in enumerate(line_list):
            split_list = str(l_t).split()
            if len(split_list) > 0:
                # 第一行完整的数据
                if index == 0:
                    if split_list[0] in start_word:
                        line_info = split_list
                    else:
                        line_info.append("")
                        line_info.extend(split_list)
                else:
                    for s_i, s_l in enumerate(split_list):
                        if re_startswith(s_l, bill_code_prefix):
                            line_info.append(split_list[s_i])
                        else:
                            material_list.append(split_list[s_i])
        if len(line_info) > len(df.columns):
            for i in range(across_column + 1, len(line_info)):
                if str(line_info[i]).isdigit() or str(line_info[i]) in unit:
                    line_info[across_column] = " ".join(line_info[across_column: i])
                    line_info = line_info[0: across_column + 1] + line_info[i:]
                    break
        line_info[across_column] = line_info[across_column] + " " + " ".join(material_list)
        if len(line_info) == len(df.columns):
            df.loc[len(df.index)] = line_info
        elif len(line_info) < len(df.columns):
            while len(line_info) < len(df.columns):
                line_info.append("")
            df.loc[len(df.index)] = line_info
        else:
            logger.warning(f"[{line_info}]丢弃")

    def handle_parser(self, file_dict, file_info, use_column_list, attribute_manager):
        # 文件是否存在
        if file_info[0] not in file_dict:
            raise Exception("对照文件[%s]中未找到" % file_info[0])
        # 读取文件
        file_name = file_dict[file_info[0]][0]
        # 跳过的文本
        skip_text = str(attribute_manager.value(pc.skip_text))
        # 列数
        column_number = int(file_info[1])
        # 单号前缀
        bill_code_prefix = list(attribute_manager.value(pc.bill_code_prefix).split(","))
        # 跨行列
        across_column = int(attribute_manager.value(pc.across_column))
        # 排除行
        exclude_line_list = ("應付小計:", "備注:", "應扣小計:", "除帳小計", "扣%金額", "贊助金", "總合計", "核准")
        # 单位
        unit = attribute_manager.value(pc.unit)
        if unit is None:
            unit = []
        else:
            unit = list(unit.split(","))
        # 解析pdf
        with pdfplumber.open(file_name) as pdf:
            text_list = []
            for page in pdf.pages:
                line_list = page.extract_text().splitlines()
                find = False
                for line in line_list:
                    if find:
                        if not any([el in line for el in exclude_line_list]):
                            text_list.append(line)
                    elif line.startswith(skip_text):
                        find = True
            # DataFrame
            df = pandas.DataFrame(columns=[str(r) for r in range(0, column_number)])
            if len(text_list) > 0:
                start_word = ["除帳", "應付", "應扣"]
                new_line = False
                line_list = []
                line_info: List[Any] = []
                for text in text_list:
                    split_list = text.split()
                    if len(split_list) > 0:
                        if split_list[0] in start_word or format_date(split_list[0]):
                            new_line = True
                        else:
                            line_list.append(text)
                        if new_line:
                            new_line = False
                            if len(line_list) > 0:
                                self._new_line(df=df,
                                               line_list=line_list,
                                               line_info=line_info,
                                               start_word=start_word,
                                               bill_code_prefix=bill_code_prefix,
                                               across_column=across_column,
                                               unit=unit)
                                line_list = []
                                line_info = []
                            line_list.append(text)

                if len(line_list) > 0:
                    self._new_line(df=df,
                                   line_list=line_list,
                                   line_info=line_info,
                                   start_word=start_word,
                                   bill_code_prefix=bill_code_prefix,
                                   across_column=across_column,
                                   unit=unit)
            # 替换空字符串
            df['0'].replace("", method="pad", inplace=True)
            # 去除无用的列
            df.columns = [str(column) for column in df.columns]
            useless_column = []
            for value in df.columns:
                if value not in use_column_list:
                    useless_column.append(value)
            if len(useless_column) > 0:
                df.drop(useless_column, axis=1, inplace=True, errors="ignore")

            return df
