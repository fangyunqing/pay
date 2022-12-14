# @Time    : 22/06/22 9:12
# @Author  : fyq
# @File    : pay_manager.py
# @Software: PyCharm

__author__ = 'fyq'

from pay.ar_day_pay import ARDayPay
from pay.check_pay import CheckPay
from pay.multiple_map_pay import MultipleMapPay
from pay.pdf_py import PdfPay
from pay.supplier_pay import SupplierPay
from pay.group_pay import GroupPay
from util.model_util import ModelUtil
from pay.dept_pay import DeptPay
from pay.reconciliation_pay import ReconciliationPay


class PayManager:

    def __init__(self):
        self.calls = 3
        self.pay_list = [SupplierPay(), GroupPay(), DeptPay(), ARDayPay(),
                         ReconciliationPay(), PdfPay(), MultipleMapPay(),
                         CheckPay()]

    @staticmethod
    def _is_ignore_file(file):
        return file.startswith("~") or file in (".", "..") or not file.endswith((".xlsx", ".xls"))

    def parse(self, angle, model_name, path, template_file):
        attribute_data = ModelUtil(angle).read_file_only(model_name)
        for pay in self.pay_list:
            p, p_n = pay.pay_name()
            if p == angle:
                pay.parse(attribute_data=attribute_data,
                          path=path,
                          template_file=template_file)

