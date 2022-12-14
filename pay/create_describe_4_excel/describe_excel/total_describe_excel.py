# @Time    : 22/12/20 14:34
# @Author  : fyq
# @File    : total_describe_excel.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.create_describe_4_excel.describe_excel.describe_excel import DescribeExcel


class TotalDescribeExcel(DescribeExcel):

    """
        统计功能
    """

    def __init__(self):
        super(TotalDescribeExcel, self).__init__()
        self.total_row = None
        self.first_row_index = None
        self.detail = None
        self.dt_column = None
