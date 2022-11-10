# @Time    : 22/11/09 11:28
# @Author  : fyq
# @File    : wei_lin_pdf_handle_parser.py
# @Software: PyCharm

__author__ = 'fyq'

import pandas
import pdfplumber

from pay.handle_parser.handle_parser import HandleParser
from util import format_date


class WeiLinPdfHandleParser(HandleParser):

    @staticmethod
    def _new_line(df, line_list, line_info, start_word):
        material_list = []
        for index, l_t in enumerate(line_list):
            split_list = str(l_t).split()
            if len(split_list) > 0:
                # 第一行完整的数据
                if index == 0:
                    if split_list[0] == start_word:
                        line_info = split_list
                    else:
                        line_info.append(start_word)
                        line_info.extend(split_list)
                else:
                    for s_i, s_l in enumerate(split_list):
                        if s_l.startswith("DGS"):
                            line_info.append(split_list.pop(s_i))
                            break
                    material_list.extend(split_list)
        if len(line_info) > len(df.columns):
            for i in range(4, len(line_info)):
                if str(line_info[i]).isdigit():
                    line_info[3] = " ".join(line_info[3: i])
                    line_info = line_info[0: 4] + line_info[i:]
                    break
        line_info[3] = line_info[3] + " " + " ".join(material_list)
        df.loc[len(df.index)] = line_info

    def handle_parser(self, file_dict, file_info, use_column_list):
        # 文件是否存在
        if file_info[0] not in file_dict:
            raise Exception("对照文件[%s]中未找到" % file_info[0])
        # 读取文件
        file_name = file_dict[file_info[0]][0]
        # 跳过的文本
        skip_text = "採購單號"
        # 解析pdf
        with pdfplumber.open(file_name) as pdf:
            text_list = []
            for page in pdf.pages:
                line_list = page.extract_text().splitlines()
                find = False
                for line in line_list:
                    if find:
                        if "應付小計:" not in line and "備注:" not in line and "應扣" not in line:
                            text_list.append(line)
                    elif line.startswith(skip_text):
                        find = True
            # 12列 DataFrame
            df = pandas.DataFrame(columns=[str(r) for r in range(0, 12)])
            if len(text_list) > 0:
                start_word = text_list[0].split()[0]
                new_line = False
                line_list = []
                line_info = []
                for text in text_list:
                    split_list = text.split()
                    if len(split_list) > 0:
                        if split_list[0] == start_word or format_date(split_list[0]):
                            new_line = True
                        else:
                            line_list.append(text)
                        if new_line:
                            new_line = False
                            if len(line_list) > 0:
                                self._new_line(df=df,
                                               line_list=line_list,
                                               line_info=line_info,
                                               start_word=start_word)
                                line_list = []
                                line_info = []
                            line_list.append(text)

                if len(line_list) > 0:
                    self._new_line(df=df,
                                   line_list=line_list,
                                   line_info=line_info,
                                   start_word=start_word)

            # 去除无用的列
            df.columns = [str(column) for column in df.columns]
            useless_column = []
            for value in df.columns:
                if value not in use_column_list:
                    useless_column.append(value)
            if len(useless_column) > 0:
                df.drop(useless_column, axis=1, inplace=True, errors="ignore")

            return df
