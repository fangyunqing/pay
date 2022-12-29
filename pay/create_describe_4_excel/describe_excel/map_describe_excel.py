# @Time    : 22/12/20 14:37
# @Author  : fyq
# @File    : map_describe_excel.py
# @Software: PyCharm

__author__ = 'fyq'


from pay.create_describe_4_excel.describe_excel.describe_excel import DescribeExcel


class MapDescribeExcel(DescribeExcel):

    """
        对账的生成
    """

    def __init__(self):
        super(MapDescribeExcel, self).__init__()
