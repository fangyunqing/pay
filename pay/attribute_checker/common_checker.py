# @Time    : 22/08/11 11:50
# @Author  : fyq
# @File    : common_checker.py
# @Software: PyCharm

__author__ = 'fyq'

from datetime import datetime


class CommonChecker:
    excel_map = {
        "A": "0", "B": "1", "C": "2", "D": "3",
        "E": "4", "F": "5", "G": "6", "H": "7",
        "I": "8", "J": "9", "K": "10", "L": "11",
        "M": "12", "N": "13", "O": "14", "P": "15",
        "Q": "16", "R": "17", "S": "18", "T": "19",
        "U": "20", "V": "21", "W": "22", "X": "23",
        "Y": "24", "Z": "25", "AA": "26", "AB": "27",
        "AC": "28", "AD": "29", "AE": "30", "AF": "31",
        "AG": "32", "AH": "33", "AI": "34", "AJ": "35",
        "AK": "36", "AL": "37", "AM": "38", "AN": "39",
        "AO": "40", "AP": "41", "AQ": "42", "AR": "43",
        "AS": "44", "AT": "45", "AU": "46", "AV": "47",
        "AW": "48", "AX": "49", "AY": "50", "AZ": "51",
    }

    @classmethod
    def check_digit(cls, key, val):
        try:
            float_val = float(val)
            str_val = str(val)
            if float_val.is_integer():
                find_index = str_val.find(".")
                if find_index > -1:
                    return int(str_val[0:find_index])
                else:
                    return int(float_val)
            else:
                raise Exception("配置项[%s]:[%s]不是整数" % (key, val))
        except ValueError:
            raise Exception("配置项[%s]:[%s]不是整数" % (key, val))

    @classmethod
    def check_digit_ge(cls, key, val):
        int_val = cls.check_digit(key, val)
        return int_val if int_val >= 0 else 0

    @classmethod
    def check_strip_len(cls, key, val, required):
        if val is None:
            val = ""
        str_val = str(val).strip()
        if len(str_val) == 0 and required:
            raise Exception("配置项[%s]:[%s]不能为空" % (key, val))
        return str_val

    @classmethod
    def check_excel_map(cls, key, val):
        key = key.upper()
        if val in cls.excel_map.keys():
            return cls.excel_map[val]
        else:
            return str(cls.check_digit(key, val))

    @classmethod
    def get_excel_column(cls, val):
        key_list = list(filter(lambda k: cls.excel_map.get(k) == str(val), cls.excel_map.keys()))
        return key_list[0] if len(key_list) > 0 else None

    @classmethod
    def check_write_sheet(cls, key, val):
        val_list = val.split(",")
        if len(val_list) < 2:
            raise Exception("配置项[%s]:[%s]格式必须为 eg: 应付汇总,4" % (key, val))

        w_s = val_list[0]
        w_r = val_list[1]
        w_c = None
        if len(val_list) > 2:
            w_c = val_list[2]
        w_s = cls.check_strip_len(key, w_s, True)
        w_r = cls.check_digit(key, w_r)
        if w_c is not None:
            w_c = cls.check_excel_map(key, w_c)
        else:
            w_c = "0"
        return w_s + "," + str(w_r) + "," + str(w_c)

    @classmethod
    def check_subtraction(cls, key, val):
        """
            减法的形式
            3-4-5,6-7-8
            A-B-C,D-E-F
        :param key: key
        :param val: val
        :return:
        """

        subtraction_exp_list = []
        for subtraction_exp in val.split(","):
            if len(subtraction_exp) <= 0:
                continue
            subtraction_list = []
            for subtraction in subtraction_exp.split("-"):
                cls.check_excel_map(key, subtraction)
                subtraction_list.append(cls.check_excel_map(key, subtraction))
            if len(subtraction_list) > 0:
                subtraction_exp_list.append("-".join(subtraction_list))

        if len(subtraction_exp_list) > 0:
            return ",".join(subtraction_exp_list)
        else:
            raise Exception("配置项[%s]:[%s]格式必须为 eg: A-B-C 或者 3-4-5" % (key, val))

    @classmethod
    def check_sheet_info(cls, key, val):
        """
            检测sheet eg 文件名，工作簿名称，跳过的行数
        :param key:
        :param val:
        :return:
        """
        sheet_info_list = list(val.split(","))
        if len(sheet_info_list) == 1:
            raise Exception("配置项[%s]:[%s]格式必须为 文件名，工作簿名称，跳过的行数" % (key, val))
        if len(sheet_info_list) == 2:
            sheet_info_list.append(0)
        return ",".join(sheet_info_list)

    @classmethod
    def check_date(cls, key, val):
        """
            检测字符是否为时间
        :param key:
        :param val:
        :return:
        """
        try:
            datetime.strptime(val, "%Y-%m-%d")
            return val
        except Exception:
            raise Exception("配置项[%s]:[%s]不是一个有效时间格式" % (key, val))
