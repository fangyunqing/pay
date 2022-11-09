# @Time    : 22/08/05 16:42
# @Author  : fyq
# @File    : interface_pay.py
# @Software: PyCharm

__author__ = 'fyq'

from abc import ABCMeta, abstractmethod

from pay.attribute_checker.default_attribute_checker import DefaultAttributeChecker
from pay.attribute.attribute import Attribute
from pay.decorator.pay_log import PayLog
from pay.path_parser import DefaultPathParser
from pay.file_copy import DefaultFileCopy
from pay.attribute.attribute_manager import AttributeManager
from pay.file_parser.file_parser import FileParser
from loguru import logger


class InterfacePay(metaclass=ABCMeta):
    """
    parse
        _set_attribute
        _check_attribute
        _parse_path
        _copy_file
        _parse_file
            _parse_file
            _reset_index
            _check
            _create_describe_4_excel
            _write_excel
            _render_target
    """

    def __init__(self):
        # 属性管理
        self._attribute_manager_dict = {"other": AttributeManager()}
        # 创建属性
        self._create_attribute_list()
        # 检查器
        self._attribute_checker_list = [DefaultAttributeChecker()]
        # 路径解析
        self._path_parser = DefaultPathParser()
        # 文件拷贝
        self._file_copy = DefaultFileCopy()
        # 文件解析
        self._file_parser = None

    def _create_attribute_list(self):
        am = self._attribute_manager_dict["other"]
        am.add(Attribute(name="read_sheet",
                         value="",
                         text="[解析]读取的工作簿名称",
                         data_type="str",
                         required=True))
        am.add(Attribute(name="skip_rows",
                         value="",
                         text="[解析]跳过的行数",
                         data_type="int",
                         required=True))
        am.add(Attribute(name="use_column",
                         value="",
                         text="[解析]需要的列(从0开始,逗号分隔)",
                         data_type="str",
                         required=True))
        am.add(Attribute(name="use_column",
                         value="",
                         text="[解析]需要的列(从0开始,逗号分隔)",
                         data_type="str",
                         required=True))
        am.add(Attribute(name="sort_column",
                         value="",
                         text="[解析]排序列",
                         data_type="str",
                         required=True))
        am.add(Attribute(name="supplier_column",
                         value="",
                         text="[解析]供应商列号",
                         data_type="str",
                         required=True))
        am.add(Attribute(name="type_column",
                         value="",
                         text="[解析]供应商类型列号",
                         data_type="str",
                         required=True))
        am.add(Attribute(name="write_sheet",
                         value="",
                         text="[模板]写入的工作簿名称",
                         data_type="str",
                         required=True))
        am.add(Attribute(name="check",
                         value="",
                         text="[模板]校对",
                         data_type="str",
                         required=False))

    def parse(self, attribute_data, path, template_file):

        logger.info("开始处理模块[%s]" % self.pay_name()[1])
        # 解析路径
        prefix_date, file_dict, target = self._path_parser.parse_path(path=path, date_length=6)
        # 拷贝模板文件
        target_file = self._file_copy.copy_file(template_file=template_file,
                                                path=path,
                                                target=target,
                                                prefix_date=prefix_date)

        for attribute_name in attribute_data.keys():
            try:
                logger.info("开始处理节点[%s]" % attribute_name)
                # 设置属性
                self._set_attribute(attribute_data[attribute_name], attribute_name)
                # 检查属性
                self._check_attribute(attribute_name)
                # 原始属性
                am = self.attribute_list(attribute_name)
                # 解析文件
                if isinstance(self._file_parser, FileParser):
                    self._file_parser.parse_file(file_dict=file_dict,
                                                 target_file=target_file,
                                                 attribute_manager=am)
                elif isinstance(self._file_parser, list):
                    pay_type = self.pay_type(attribute_name, am)
                    for fp in self._file_parser:
                        if isinstance(fp, FileParser) and fp.support(pay_type):
                            fp.parse_file(file_dict=file_dict,
                                          target_file=target_file,
                                          attribute_manager=am)
            except Exception as e:
                raise Exception("处理节点[%s]失败:[%s]" % (attribute_name, str(e)))

            logger.info("结束处理节点[%s]" % attribute_name)

        logger.info("结束处理模块[%s]" % self.pay_name()[1])

    def _set_attribute(self, attribute_dict, pay_option):
        """
            设置属性
        :param attribute_dict: 属性字典
        :return:
        """
        am = self.attribute_list(pay_option)
        for attribute in am.attribute_list:
            if attribute.name in attribute_dict:
                attribute.value = attribute_dict[attribute.name]
            else:
                attribute.value = ""

    @PayLog(node="属性检查")
    def _check_attribute(self, pay_option):
        am = self.attribute_list(pay_option)
        for _attribute_checker in self._attribute_checker_list:
            _attribute_checker.check_attribute(am.attribute_list)

    def attribute_list(self, pay_option):
        map_p_o = self.map_pay_option(pay_option)
        for key in self._attribute_manager_dict.keys():
            if map_p_o in key.split(","):
                return self._attribute_manager_dict[key]
        return self._attribute_manager_dict["other"]

    def map_pay_option(self, pay_option):
        for po in self.pay_options():
            if po[1] == pay_option:
                return po[0]

    @abstractmethod
    def pay_name(self):
        pass

    @abstractmethod
    def pay_options(self):
        pass

    def pay_type(self, attribute_name, am):
        return self.pay_name()[0] + "." + self.map_pay_option(attribute_name)