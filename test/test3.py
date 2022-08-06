# @Time    : 22/07/23 8:04
# @Author  : fyq
# @File    : test3.py
# @Software: PyCharm

__author__ = 'fyq'

from frame.label_edit_frame import CollapsingFrame
import ttkbootstrap as ttk

if __name__ == "__main__":
    app = ttk.Window("PC Cleaner", "pulse")
    CollapsingFrame(app, attribute={"name": "user", "text": "用户名"}).pack(side=ttk.TOP, fill=ttk.X)
    CollapsingFrame(app, attribute={"name": "user", "text": "密码"}).pack(side=ttk.TOP, fill=ttk.X)
    app.geometry("750x500")
    app.position_center()
    app.mainloop()
