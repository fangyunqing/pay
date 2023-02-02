# @Time    : 22/12/16 13:17
# @Author  : fyq
# @File    : common_attribute.py
# @Software: PyCharm

__author__ = 'fyq'

from .attribute import Attribute
from pay.constant import attr_string

# 校对基点
check_point_attr = Attribute(name=attr_string.check_point,
                             text="校对基点",
                             data_type="int",
                             required=True)

# 金额列
money_column_attr = Attribute(name=attr_string.money_column,
                              text="[解析]金额列(eg: A or 1)",
                              data_type="str",
                              required=True)

# 数量
qty_column_attr = Attribute(name=attr_string.qty_column,
                            text="[解析]数量列(eg: A or 1)",
                            data_type="str",
                            required=True)

# 税率列
rate_column_attr = Attribute(name=attr_string.rate_column,
                             text="[解析]税率列(eg: A or 1)",
                             data_type="str",
                             required=True)

# 类别列
kind_column_attr = Attribute(name=attr_string.kind_column,
                             text="[解析]类别列(eg: A or 1)",
                             data_type="str",
                             required=True)

# 用途列
use_column_attr = Attribute(name=attr_string.use_column,
                            text="[解析]用途列(eg: A or 1)",
                            data_type="str",
                            required=True)

# 客户编码列
client_code_column_attr = Attribute(name=attr_string.client_code_column,
                                    text="[解析]客户编码列(eg: A or 1)",
                                    data_type="str",
                                    required=True)
# 数据文件
data_file_attr = Attribute(name=attr_string.data_file,
                           text="数据文件[文件名,工作簿名,跳过的行数]",
                           data_type="str",
                           required=True)

# 读取的工作簿
read_sheet_attr = Attribute(name=attr_string.read_sheet,
                            text="[解析]读取的工作簿名称",
                            data_type="str",
                            required=True)

# 跳过的行数
skip_rows_attr = Attribute(name=attr_string.skip_rows,
                           text="[解析]跳过的行数",
                           data_type="int",
                           required=True)

# 首列是否单元格合并
first_column_merger_attr = Attribute(name=attr_string.first_column_merger,
                                     text="first_column_merger",
                                     data_type="int",
                                     required=False)

# 用到列
use_columns_attr = Attribute(name=attr_string.use_columns,
                             text="[解析]需要的列(eg: A,B or 1,2)",
                             data_type="str",
                             required=True)

# 写入的工作簿信息 工作簿,跳过的行,跳过的列
write_sheet_attr = Attribute(name=attr_string.write_sheet,
                             text="[模板]写入的工作簿名称[工作簿名,跳过的行,跳过的列]",
                             data_type="str",
                             required=True)
