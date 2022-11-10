# @Time    : 22/11/09 11:20
# @Author  : fyq
# @File    : wei_lin_pdf_file_parser.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.create_describe_4_excel.default_create_describe_4_excel import DefaultCreateDescribe4Excel
from pay.file_parser.abstract_pdf_file_parser import AbstractPdfFileParser
from pay.handle_parser.wei_lin_pdf_handle_parser import WeiLinPdfHandleParser
from pay.render.default_render import DefaultRender
from pay.write_excel.default_write_excel import DefaultWriteExcel
import pay.constant as pc


class WeiLinPafFileParser(AbstractPdfFileParser):

    def _do_parse_pdf(self, file_dict, attribute_manager):
        map_file_info = str(attribute_manager.value(pc.pdf_file)).split(",")
        map_use_column_list = list(attribute_manager.value(pc.use_column).split(","))
        map_df = WeiLinPdfHandleParser().handle_parser(file_dict=file_dict,
                                                       file_info=map_file_info,
                                                       use_column_list=map_use_column_list)
        map_df.dropna(inplace=True)
        return [map_df]

    def _do_create_describe_4_excel(self, df, attribute_manager):
        return DefaultCreateDescribe4Excel().create_describe_4_excel(df_list=df,
                                                                     attribute_manager=attribute_manager)

    def _do_write_excel(self, describe_excel, attribute_manager, target_file):
        DefaultWriteExcel().write_excel(describe_excel, attribute_manager, target_file)

    def _do_render_target(self, describe_excel_list, attribute_manager, target_file):
        DefaultRender().render(describe_excel_list, attribute_manager, target_file)

    def support(self, pay_type):
        return "威霖"
