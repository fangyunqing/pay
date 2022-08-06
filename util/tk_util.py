# @Time    : 22/08/04 13:33
# @Author  : fyq
# @File    : tk_util.py
# @Software: PyCharm

__author__ = 'fyq'

from ttkbootstrap.dialogs import MessageDialog
from ttkbootstrap.icons import Icon


class MessageBoxUtil:

    @staticmethod
    def show_error(parent, message, title=" ", alert=True, **kwargs):
        dialog = MessageDialog(
            message=message,
            title=title,
            parent=parent,
            buttons=["OK:primary"],
            icon=Icon.error,
            alert=alert,
            localize=True,
            **kwargs,
        )

        dialog._result = None
        dialog.build()
        dialog.update_idletasks()

        x = parent.winfo_rootx()
        y = parent.winfo_rooty()
        w = parent.winfo_width()
        h = parent.winfo_height()
        d_w = dialog.winfo_width()
        d_h = dialog.winfo_height()

        diff_w = w - d_w
        diff_h = h - d_h
        if diff_w > 0:
            p_x = x + diff_w/2
        else:
            p_x = x

        if diff_h > 0:
            p_y = x + diff_h/2
        else:
            p_y = y

        dialog.show(position=(p_x, p_y))


