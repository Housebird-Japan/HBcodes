from PIL import Image as piImange
import pyocr
import pyocr.builders
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import *
import logging


# ボタンクリックイベント
def btn_click():
    sub_window()
    try:
        num = var.get()
        if num == '':
            exit()
        image_name = EditBox.get()
        if image_name == '':
            exit()
        cols = EditBox3.get()
        if cols == '':
            exit()
        file_name = EditBox2.get()
        if file_name == '':
            exit()
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            sys.exit(1)
        tool = tools[0]

        txt = tool.image_to_string(
         piImange.open(image_name),
         builder=pyocr.builders.TextBuilder()
        )

        txt.replace('o', '0')
        textlist = txt.split()
        del textlist[0]
        nplist = list(np.array_split(textlist, cols))
        df = pd.DataFrame(nplist)
        file_name = file_name.replace('.csv', '').replace('.xlsx', '').replace('.xls', '')
        if num == 0:
            df.to_csv(file_name + '.csv',
                      index=False,
                      mode='a'
                      )
        else:
            with pd.ExcelWriter(file_name + '.xlsx') as writer:
                df.to_excel(writer)
        root.destroy()
    except Exception as other:
        logger = logging.getLogger('LoggingTest')
        logger.setLevel(10)
        sh = logging.StreamHandler()
        logger.addHandler(sh)
        fh = logging.FileHandler('error.log', encoding='UTF-8')
        logger.addHandler(fh)
        formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        logger.log(30, other)


class Progressbar(ttk.LabelFrame):

    def __init__(self, master=None):
        super().__init__(master, text="進捗")
        self.progress = ttk.Progressbar(self)
        self.progress.configure(
            value=0,
            mode='indeterminate',
            maximum=100
            )
        self.progress.pack()
        self.progress.start(interval=10)


def sub_window():
    sub_win = Toplevel()
    sub_win.geometry("300x150")
    f = Progressbar(master=sub_win)
    f.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.title(u"ASUKARU　画像データ処理")
    root.geometry("400x300")
    Label1 = tk.Label(text=u'解析する画像ファイルの名前')
    Label1.place(x=10, y=10)
    EditBox = tk.Entry(width=50)
    EditBox.place(x=10, y=30)

    Label3 = tk.Label(text=u'解析する画像の行数')
    Label3.place(x=10, y=50)
    EditBox3 = tk.Entry(width=50)
    EditBox3.insert(tk.END, "数字で入力してください。")
    EditBox3.place(x=10, y=70)

    # チェック有無変数
    Label2 = tk.Label(text=u'出力ファイル形式')
    Label2.place(x=10, y=100)
    var = tk.IntVar()
    var.set(0)

    rdo1 = tk.Radiobutton(value=0, variable=var, text='CSV')
    rdo1.place(x=70, y=120)
    rdo2 = tk.Radiobutton(value=1, variable=var, text='Excel')
    rdo2.place(x=150, y=120)

    # 出力ファイル名ラベル
    Label2 = tk.Label(text=u'出力ファイル名')
    Label2.place(x=10, y=170)

    EditBox2 = tk.Entry(width=50)
    EditBox2.place(x=10, y=200)

    # Button = tk.Button(text=u'処理開始', width=50, command=sub_window)
    Button = tk.Button(text=u'処理開始', width=50, command=btn_click)
    Button.place(x=10, y=240)

    root.mainloop()
