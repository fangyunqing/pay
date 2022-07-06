import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pay.pay_manager import PayManager
import threading
from tkinter import messagebox
import time
import traceback
from util.model_util import ModelUtil


def save():
    md = ModelUtil("pay")
    md.write_file("default", option_list)


def print_exception(e):
    traceback.print_exc()
    err_msg = repr(e) + "\n" + traceback.format_exc()
    messagebox.showerror("错误", err_msg)


def print_msg(msg):
    tx_msg.insert(tk.END, msg)
    tx_msg.insert(tk.INSERT, '\n')
    tx_msg.see(tk.END)
    tx_msg.update()


def set_in_screen_center(tk_widget, win_width=None, win_height=None):
    # 获取根窗口
    root = tk_widget
    temp_root = None
    while 1:
        temp_root = root.master
        if temp_root is None:
            break
        root = temp_root
    # 获取屏幕分辨率
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    if win_width is None or win_height is None:
        root.update()
    if win_width is None:
        win_width = tk_widget.winfo_width()
    if win_height is None:
        win_height = tk_widget.winfo_height()

    x = int((screen_width - win_width) / 2)
    y = int((screen_height - win_height) / 2)

    # 设置窗口初始位置在屏幕居中
    tk_widget.geometry("%sx%s+%s+%s" % (win_width, win_height, x, y))


def choice(angle):
    def choice_dir():
        try:
            current_dir = filedialog.askdirectory()
            if current_dir:
                str_dir.set(current_dir)
                option_set["dir"] = current_dir
        except Exception as e:
            print_exception(e)

    def choice_file():
        try:
            current_file = filedialog.askopenfilename(filetypes=[('xlsx', '*.xlsx'), ('xls', '*.xls')], )
            if current_file:
                str_file.set(current_file)
                option_set["file"] = current_file
        except Exception as e:
            print_exception(e)

    if angle not in option_list:
        option_list[angle] = {}

    option_set = option_list.get(angle)

    child = tk.Toplevel(window)
    child.title("设置")
    child.grab_set()
    child.transient(window)
    child.iconbitmap('ico/bitbug_favicon.ico')
    set_in_screen_center(child, win_width=400)
    bt_choice_dir = tk.Button(child, text="选择文件夹", command=choice_dir)
    bt_choice_dir.place(x=10, y=10)
    str_dir = tk.StringVar()
    str_dir.set(option_set.get("dir", ""))
    et_dir = tk.Entry(child, show=None, width=50, textvariable=str_dir, justify='left')
    et_dir.place(x=10, y=50)
    bt_choice_file = tk.Button(child, text="选择模板文件", command=choice_file)
    bt_choice_file.place(x=10, y=90)
    str_file = tk.StringVar()
    str_file.set(option_set.get("file", ""))
    et_file = tk.Entry(child, show=None, width=50, textvariable=str_file, justify='left')
    et_file.place(x=10, y=130)


def set_use_option(angle):
    def save():
        try:
            model_name = cb_model.get()
            md.write_file(model_name, fr_dict)
            cb_model["values"] = md.model_list
            if angle == "supplier":
                cb_supplier["values"] = md.model_list
            else:
                cb_group["values"] = md.model_list
        except Exception as ex:
            print_exception(ex)

    def model_select(event):
        try:
            model_name = cb_model.get()
            md.read_file(model_name, fr_dict)
        except Exception as ex:
            print_exception(ex)

    def create_option(key, text, val_type, row):
        if val_type == 0:
            val = tk.StringVar()
        else:
            val = tk.IntVar()

        fr_info[key] = val
        tk.Label(fr, text=text, ).grid(row=row, column=0, padx=10, pady=5)
        tk.Entry(fr, textvariable=val).grid(row=row, column=1)

    try:
        if angle not in option_list:
            option_list[angle] = {}

        child = tk.Toplevel(window)
        child.title("设置常用项")
        child.grab_set()
        child.transient(window)
        child.iconbitmap('ico/bitbug_favicon.ico')
        set_in_screen_center(child, win_width=400, win_height=350)

        option_set = option_list.get(angle)

        option_note = ttk.Notebook(child)
        option_note.pack(fill=tk.X, expand=True, side=tk.TOP)

        pl_bottom = ttk.Frame(child)
        pl_bottom.pack(fill=tk.X, expand=True, side=tk.BOTTOM)
        cb_model = ttk.Combobox(pl_bottom)
        cb_model.bind("<<ComboboxSelected>>", model_select)
        cb_model.grid(padx=10)
        tk.Button(pl_bottom, text="保存", command=save).grid(row=0, column=1, padx=10)

        md = ModelUtil(angle)
        cb_model["values"] = md.model_list
        fr_dict = {}
        for name in option_set.get("option"):
            row_index = 0
            fr_info = {}
            fr_dict[name] = fr_info
            fr = ttk.Frame(child, relief='ridge', borderwidth=1)
            option_note.add(fr, text=name)
            create_option("read_sheet", "读取的工作簿名称", 0, row=row_index)
            row_index = row_index + 1
            create_option("write_sheet", "写入的工作簿名称", 0, row=row_index)
            row_index = row_index + 1
            if angle == "supplier":
                create_option("write_detail_sheet", "写入的详情工作簿名称", 0, row=row_index)
                row_index = row_index + 1
            create_option("use_column", "需要的列(从0开始,逗号分隔)", 0, row=row_index)
            row_index = row_index + 1
            create_option("skip_rows", "跳过的行数", 1, row=row_index)
            row_index = row_index + 1
            create_option("supplier_column", "供应商列号", 1, row=row_index)
            row_index = row_index + 1
            create_option("type_column", "供应商类型列号", 1, row=row_index)
            row_index = row_index + 1
            create_option("date_location", "截止时间位置(行列,从1开始)", 0, row=row_index)
            row_index = row_index + 1
            create_option("title_rows", "标题行数", 1, row=row_index)
    except Exception as e:
        print_exception(e)


def callback(msg):
    pg["value"] = pg["value"] + 1
    print_msg(msg)


def thread_func(info_list):
    pay_manager = PayManager()
    pg['maximum'] = len(info_list) * pay_manager.calls
    pg["value"] = -1
    tx_msg.delete(1.0, tk.END)
    window.attributes("-disabled", True)
    begin_time = time.time()
    md = ModelUtil("supplier")
    try:
        for info in info_list:
            pay_manager.parse(info[3], info[4], info[0], info[1], callback, target=info[2])
        print_msg("总共用时：{:.2f}秒".format(time.time() - begin_time))
    except Exception as e:
        print_exception(e)
    finally:
        pg['maximum'] = 0
        window.attributes("-disabled", False)


def start():
    info_list = []
    for key in option_list:
        value = option_list[key]
        val = value.get("val").get()
        path = value.get("dir", "").strip()
        model = value.get("file", "").strip()
        target = value.get("target", "").strip()
        model_file = value.get("model_name").get()
        if val == 1 and len(path) > 0 and len(model) > 0:
            info_list.append((path, model, target, key, model_file))

    if len(info_list) > 0:
        t = threading.Thread(target=thread_func, args=(info_list,))
        t.setDaemon(True)
        t.start()


window = tk.Tk()
set_in_screen_center(window, 380, 500)
window.resizable(0, 0)
window.iconbitmap('ico/bitbug_favicon.ico')
# 供应商
ck_supplier_val = tk.IntVar()
ck_supplier = tk.Checkbutton(window,
                             text="供应商维度",
                             variable=ck_supplier_val,
                             onvalue=1,
                             offvalue=0)
ck_supplier.place(x=10, y=10)
bt_supplier = tk.Button(window, text="设置文件和模板", command=lambda: choice("supplier"))
bt_supplier.place(x=100, y=10)
bt_set_supplier = tk.Button(window, text="设置常用项", command=lambda: set_use_option("supplier"))
bt_set_supplier.place(x=200, y=10)
cb_supplier = ttk.Combobox(window, values=ModelUtil("supplier").model_list)
cb_supplier.place(x=280, y=12, width=80)
# 集团
ck_group_val = tk.IntVar()
ck_group = tk.Checkbutton(window,
                          text="集团维度",
                          variable=ck_group_val,
                          onvalue=1,
                          offvalue=0)
ck_group.place(x=10, y=50)
bt_group = tk.Button(window, text="设置文件和模板", command=lambda: choice("group"))
bt_group.place(x=100, y=50)
bt_set_group = tk.Button(window, text="设置常用项", command=lambda: set_use_option("group"))
bt_set_group.place(x=200, y=50)
cb_group = ttk.Combobox(window, values=ModelUtil("group").model_list)
cb_group.place(x=280, y=52, width=80)
# 其他
bt_start = tk.Button(window, text="开始", command=start)
bt_start.place(x=10, y=90)
bt_start = tk.Button(window, text="保存配置项", command=save)
bt_start.place(x=50, y=90)
pg = ttk.Progressbar(window)
pg.place(x=10, y=140)
pg.pack_forget()
pg['length'] = 350
tx_msg = tk.Text(window, height=24, width=52)
tx_msg.place(x=1, y=220, anchor='nw')
# 全局配置项
option_list = {
    "supplier": {"val": ck_supplier_val,
                 "target": "供应商维度",
                 "option": ["应付汇总", "预付汇总"],
                 "model_name": cb_supplier},
    "group": {"val": ck_group_val,
              "target": "集团维度",
              "option": ["应付汇总", "应付未付款", "预付汇总"],
              "model_name": cb_group}
}
mdd = ModelUtil("pay")
mdd.read_file("default", option_list)
window.mainloop()
