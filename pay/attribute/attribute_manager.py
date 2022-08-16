# @Time    : 22/08/11 15:55
# @Author  : fyq
# @File    : attribute_manager.py
# @Software: PyCharm

__author__ = 'fyq'


class AttributeManager:
    """
        属性管理
    """

    def __init__(self):
        self.attribute_list = []

    def add(self, attribute):
        """
            添加属性
        :param attribute: 属性
        :return:
        """
        self.delete(attribute.name)
        self.attribute_list.append(attribute)

    def delete(self, name):
        """
            删除属性
        :param name: 属性名称
        :return:
        """
        index_list = []
        for index, attr in enumerate(self.attribute_list):
            if name == attr.name:
                index_list.append(index)
        index_list.reverse()
        for index in index_list:
            self.attribute_list.pop(index)

    def insert(self, name, attribute, where="after"):
        """
            指定位置前或后插入值
        :param where: 位置
        :param name:  属性名称
        :param attribute: 属性
        :return:
        """
        find_index = [index for index, attribute in enumerate(self.attribute_list)
                      if attribute.name == name]
        self.delete(attribute.name)
        if len(find_index) > 0:
            if where == "after":
                self.attribute_list.insert(find_index[0] + 1, attribute)
            else:
                self.attribute_list.insert(find_index[0], attribute)
        else:
            self.attribute_list.append(attribute)

    def value(self, name):
        """
            返回属性值
        :param name: 属性名称
        :return:
        """
        value_list = [attribute.value for attribute in self.attribute_list if attribute.name == name]
        if len(value_list) > 0:
            return value_list[0]

    def get(self, name):
        """
            返回属性值
        :param name:
        :return:
        """
        value_list = [attribute for attribute in self.attribute_list if attribute.name == name]
        if len(value_list) > 0:
            return value_list[0]

