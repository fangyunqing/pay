# @Time    : 22/12/17 13:14
# @Author  : fyq
# @File    : single_express.py
# @Software: PyCharm

import pay.constant as pc

__author__ = 'fyq'


class SingleExpress:

    def __init__(self, express: str):
        self.operator = ""
        if "*" in express:
            param_list = express.split("*")
            self.operator = "*"
        elif "+" in express:
            param_list = express.split("+")
            self.operator = "+"
        elif "-" in express:
            param_list = express.split("-")
            self.operator = "-"
        elif "/" in express:
            param_list = express.split("/")
            self.operator = "/"
        else:
            raise Exception(pc.error_string.map_error_50002)

        if len(param_list) != 2:
            raise Exception(pc.error_string.map_error_50001)

        self.param_one, self.param_two = [int(param) for param in param_list]

    def is_add(self):
        return self.operator == "+"

    def is_sub(self):
        return self.operator == "-"

    def is_mul(self):
        return self.operator == "*"

    def is_div(self):
        return self.operator == "/"
