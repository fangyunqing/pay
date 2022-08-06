# @Time    : 22/08/05 10:24
# @Author  : fyq
# @File    : detail_messagebox.py
# @Software: PyCharm

__author__ = 'fyq'

from ttkbootstrap.dialogs import Dialog
import ttkbootstrap as ttk


class DetailMessageBox(Dialog):

    def __init__(self, title=" ", value="", padding=(20, 20), parent=None):
        super().__init__(parent=parent, title=title)
        self._value = value
        self._padding = padding
        self._tx = None

    def create_body(self, master):
        frame = ttk.Frame(master, padding=self._padding)
        frame.pack(side=ttk.TOP, fill=ttk.BOTH, expand=ttk.YES)
        self._tx = ttk.Text(frame)
        self._tx.pack(side=ttk.TOP, fill=ttk.BOTH, expand=ttk.YES)
        self._tx.insert(ttk.END, self._value)

    def create_buttonbox(self, master):
        frame = ttk.Frame(master)
        frame.pack(side=ttk.TOP, fill=ttk.BOTH, expand=ttk.YES)
        ttk.Button(frame, text="保存", command=self.on_save) \
            .pack(side=ttk.LEFT, anchor=ttk.E, expand=ttk.YES, padx=5, pady=5)
        ttk.Button(frame, text="取消", command=self.on_cancel) \
            .pack(side=ttk.LEFT, anchor=ttk.W, expand=ttk.YES, padx=5, pady=5)

    def on_cancel(self):
        self._toplevel.destroy()

    def on_save(self):
        self._result = self._tx.get("1.0", ttk.END)
        self._toplevel.destroy()
