# @Time    : 22/12/16 13:17
# @Author  : fyq
# @File    : common_attribute.py
# @Software: PyCharm

__author__ = 'fyq'

from .attribute import Attribute
import pay.constant as pc
import pay.constant.attr_string as attr_string

check_point_attr = Attribute(name=pc.check_point,
                             value="",
                             text="校对基点",
                             data_type="int",
                             required=True)

first_merger_attr = Attribute(name=attr_string.first_merger,
                              value="",
                              text="[模板]首列是否合并",
                              required=False,
                              data_type="str")

check_attr = Attribute(name="check",
                       value="",
                       text="[模板]校对",
                       data_type="str",
                       required=False)
