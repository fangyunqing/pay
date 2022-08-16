# @Time    : 22/08/11 15:53
# @Author  : fyq
# @File    : attribute.py
# @Software: PyCharm

__author__ = 'fyq'


class Attribute:

    def __init__(self, name, value, text, data_type, required):
        """
        :param name: 名称
        :param value: 值
        :param text: 文本
        :param data_type: 类型
        :param required: 是否必填
        """
        self.name = name
        self.value = value
        self.text = text
        self.data_type = data_type
        self.required = required
