# @Time    : 22/08/12 16:23
# @Author  : fyq
# @File    : describe_excel.py
# @Software: PyCharm

__author__ = 'fyq'


class DescribeExcel:

    """
        描述excel信息 用于写入excel 和 渲染excel
    """

    def __init__(self):

        # DataFrame
        self.df = None

        # DataFrame的行数
        self.row = None

        # DataFrame的列数
        self.column = None

        # 工作簿的名称
        self.sheet_name = None

        # 工作簿的起始行 0开始
        self.start_row = None

        # 工作簿的起始列 0开始
        self.start_column = None
