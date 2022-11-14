# @Time    : 22/11/11 13:40
# @Author  : fyq
# @File    : re_util.py
# @Software: PyCharm

__author__ = 'fyq'

import re
from collections.abc import Iterable


def re_startswith(val: str, pattern):
    if isinstance(pattern, str):
        if not pattern.startswith("^"):
            pattern = "^" + pattern

        return True if re.match(pattern, val) else False

    if isinstance(pattern, Iterable):
        for s in pattern:
            if not s.startswith("^"):
                s = "^" + s
            if re.match(s, val):
                return True

    return False


if __name__ == "__main__":
    print(re_startswith("C1H0292609CO0880", "C.H"))
