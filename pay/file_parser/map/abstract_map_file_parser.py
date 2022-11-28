# @Time    : 22/09/26 15:43
# @Author  : fyq
# @File    : abstract_map_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.file_parser.file_parser import FileParser
from abc import abstractmethod
from pay.decorator.pay_log import PayLog


class AbstractMapFileParser(FileParser):
    """
        抽象基类
        通过 对照表和数据 导入到模板文件中
    """

    def parse_file(self, file_dict, target_file, attribute_manager):
        # 解析特殊列
        self._parse_spec_column(attribute_manager=attribute_manager)
        # 解析数据库对照
        map_df_list, origin_map_df = self._parse_map(file_dict, attribute_manager)
        # 解析数据
        data_df = self._parse_data(file_dict, attribute_manager)
        # 合并数据
        merger_df = self._merger(map_df_list=map_df_list,
                                 data_df=data_df,
                                 origin_map_df=origin_map_df,
                                 attribute_manager=attribute_manager)
        # 重建索引
        self._reset_index(merger_df, attribute_manager)
        # excel描述符
        describe_excel = self._create_describe_4_excel(merger_df, attribute_manager)
        # 写入excel
        self._write_excel(describe_excel, attribute_manager, target_file)
        # 渲染excel
        self._render_target(describe_excel, attribute_manager, target_file)

    @PayLog(node="解析数据对照")
    def _parse_map(self, file_dict, attribute_manager):
        return self._do_parse_map(file_dict, attribute_manager)

    @abstractmethod
    def _do_parse_map(self, file_dict, attribute_manager):
        pass

    @PayLog(node="解析数据")
    def _parse_data(self, file_dict, attribute_manager):
        return self._do_parse_data(file_dict, attribute_manager)

    @abstractmethod
    def _do_parse_data(self, file_dict, attribute_manager):
        pass

    @PayLog(node="合并数据")
    def _merger(self, map_df_list, data_df, origin_map_df, attribute_manager):
        return self._do_merger(map_df_list, data_df, origin_map_df, attribute_manager)

    @abstractmethod
    def _do_merger(self, map_df_list, data_df, origin_map_df, attribute_manager):
        pass

    @PayLog(node="重建索引")
    def _reset_index(self, df, attribute_manager):
        self._do_reset_index(df, attribute_manager)

    @abstractmethod
    def _do_reset_index(self, df, attribute_manager):
        pass

    @PayLog(node="创建excel文件描述")
    def _create_describe_4_excel(self, df, attribute_manager):
        return self._do_create_describe_4_excel(df, attribute_manager)

    @abstractmethod
    def _do_create_describe_4_excel(self, df, attribute_manager):
        pass

    @PayLog(node="写入excel")
    def _write_excel(self, describe_excel, attribute_manager, target_file):
        self._do_write_excel(describe_excel, attribute_manager, target_file)

    @abstractmethod
    def _do_write_excel(self, describe_excel, attribute_manager, target_file):
        pass

    @PayLog(node="渲染excel")
    def _render_target(self, describe_excel_list, attribute_manager, target_file):
        self._do_render_target(describe_excel_list, attribute_manager, target_file)

    @abstractmethod
    def _do_render_target(self, describe_excel, attribute_manager, target_file):
        pass

    @PayLog(node="解析特殊列")
    def _parse_spec_column(self, attribute_manager):
        self._do_parse_spec_column(attribute_manager=attribute_manager)

    @abstractmethod
    def _do_parse_spec_column(self, attribute_manager):
        pass
