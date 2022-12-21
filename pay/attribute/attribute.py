# @Time    : 22/08/11 15:53
# @Author  : fyq
# @File    : attribute.py
# @Software: PyCharm

__author__ = 'fyq'


class Attribute:

    def __init__(self, name, value, text, data_type, required, cb_values=None):
        """
        :param name: 名称
        :param value: 值
        :param text: 文本
        :param data_type: 类型
        :param required: 是否必填
        :param cb_values: 组合框的值
        """
        self.name = name
        self.value = value
        self.text = text
        self.data_type = data_type
        self.required = required
        self.cb_values = cb_values
