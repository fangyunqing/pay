# @Time    : 22/12/16 13:17
# @Author  : fyq
# @File    : common_attribute.py
# @Software: PyCharm

__author__ = 'fyq'


from .attribute import Attribute
import pay.constant as pc

check_point_attr = Attribute(name=pc.check_point,
                             value="",
                             text="校对基点",
                             data_type="int",
                             required=True)


