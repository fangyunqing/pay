# @Time    : 22/08/11 15:53
# @Author  : fyq
# @File    : attribute.py
# @Software: PyCharm

__author__ = 'fyq'

from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class Attribute:
    """
        name: 名称
        value: 值
        text: 文本
        data_type: 类型
        required: 是否必填
        cb_values: 组合框的值
    """

    name: str

    text: str

    data_type: str

    required: bool

    cb_values: List[Any] = field(default=None)

    value: str = field(default="")

    multi_line: bool = False


