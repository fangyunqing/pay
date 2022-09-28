# @Time    : 22/08/09 16:03
# @Author  : fyq
# @File    : default_file_copy.py
# @Software: PyCharm

__author__ = 'fyq'

import os
import shutil
import uuid

from loguru import logger
from pay.file_copy.file_copy import FileCopy
from pay.decorator.pay_log import PayLog


class DefaultFileCopy(FileCopy):
    """
    默认的文件拷贝
    """

    @PayLog(node="文件拷贝")
    def copy_file(self, template_file, prefix_date, path, target=None):

        """
            复制文件到path路径下
        :param template_file: 模板文件
        :param prefix_date: 时间
        :param path: 路径
        :param target: 复制文件名称 None 用模板文件的名称
        :return:
        """

        if prefix_date is None:
            prefix_date = ""

        template_name = os.path.basename(template_file)
        template_ext = os.path.splitext(template_file)[1]
        if target is None:
            target = template_name
        elif not target.endswith(template_ext):
            target = target + template_ext
        # 在path下面生成target文件夹
        target_dir = path + r"/target/"
        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)
        # 目标文件
        target_file = target_dir + prefix_date + target

        logger.info("拷贝模板文件[%s]到[%s]" % (template_file, target_file))

        try:
            if os.path.exists(target_file):
                uid = uuid.uuid1()
                tmp_file = target_file + "_" + str(uid)
                shutil.move(target_file, tmp_file)
            shutil.copy(template_file, target_file)
        except Exception:
            raise Exception("拷贝模板文件[%s]到[%s]失败" % (template_file, target_file))

        return target_file
