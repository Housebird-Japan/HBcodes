# -* UTF-8 Python3.6 *-
import urllib.request as u
from bs4 import BeautifulSoup
import time
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import *
import logging


def soup(url):
    res = u.urlopen(url)
    soup_data = BeautifulSoup(res, 'html.parser', from_encoding='UTF-8')
    return soup_data


def get_estate_urls(soup_data):
    data = soup_data.select('div.cassettebox-title > h2 > a')
    urls = [i.get('href') for i in data]
    return urls


def url_join(urls):
    join_urls = [u.urljoin('https://suumo.jp/', i) for i in urls]
    return join_urls


def clean_html(raw_html):
    clean_r = re.compile(r"<[^>]*?>")
    clean_text = clean_r.sub('', raw_html)
    return clean_text


def getdata(join_url_list):
    data_list = []
    for q in join_url_list:
        op = soup(q)
        name = op.select_one('h1').get_text()
        adrres = op.select_one('div.mt20 > table > tbody > tr:nth-child(1) > td')
        if adrres is None:
            com = op.select('table.data_table.table_gaiyou > tr > td')
            adrres = com[0].get_text()
            tel = op.select_one('.fs-big').get_text().replace('\n', '')
            fax = com[3].get_text()
            company_url = str(com[6]).replace("'", '"')\
                .replace('<td>', '').replace('<a href="javascript:void(0);" onclick="javascript:popUpMap2("', '')\
                .replace('", "01"); return false;">', '')\
                .replace('当社ＨＰはこちら', '')\
                .replace('<br>', '')\
                .replace('</a>', '')\
                .replace('</br>', '')\
                .replace('</td>', '')\
                .replace('!', '').replace('当社HPはこちら！', '').replace('\n', '').replace('-', '').replace('当社ホームページへ', '')
            print(company_url)
        else:
            adrres = adrres.get_text()
            tel = op.select_one('div.mt20 > table > tbody > tr:nth-child(2) > '
                                'td:nth-child(2) > div:nth-child(1) >'
                                ' em > span.fs18').get_text()
            fax = op.select_one('div.mt20 > table > tbody > tr:nth-child(2) > td:nth-child(4)').get_text()
            company_url = op.select_one('div.mt20 > table > tbody > tr:nth-child(4) > td > ul > li:nth-child(1) > a')
            if company_url is None:
                company_url = "-"
            else:
                company_url = company_url.get('href')
        data_list.append([name, adrres, tel, fax, company_url])
        time.sleep(1)
    return data_list


class Progressbar(ttk.LabelFrame):
    """
        プログレスバー設置
    """

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


def main():
    """　メイン処理を実行　"""
    sub_window()
    try:
        num = var.get()
        if num == '':
            exit()
        url = EditBox.get()
        if url == '':
            exit()
        file_name = EditBox2.get()
        if file_name == '':
            exit()
        file_name = file_name.replace('.csv', '').replace('.xlsx', '').replace('.xls', '')
        # 処理
        soup_data = soup(url)
        url_list = get_estate_urls(soup_data)
        data = getdata(url_join(url_list))
        # 書き出し
        if num == 0:
            with open(file_name + '.csv', 'a', newline='', encoding='UTF-8') as f:
                writer = csv.writer(f)
                writer.writerows(data)
        else:
            pass
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


if __name__ == '__main__':
    root = tk.Tk()
    root.title(u"SUMOスクレイピング")
    root.geometry("400x300")
    Label1 = tk.Label(text=u'解析するURL')
    Label1.place(x=10, y=10)
    EditBox = tk.Entry(width=50)
    EditBox.place(x=10, y=30)

    # チェック有無変数
    Label2 = tk.Label(text=u'出力ファイル形式')
    Label2.place(x=10, y=80)
    var = tk.IntVar()
    var.set(0)

    rdo1 = tk.Radiobutton(value=0, variable=var, text='CSV')
    rdo1.place(x=70, y=100)
    rdo2 = tk.Radiobutton(value=1, variable=var, text='Excel')
    rdo2.place(x=150, y=100)

    # 出力ファイル名ラベル
    Label2 = tk.Label(text=u'出力ファイル名')
    Label2.place(x=10, y=150)

    EditBox2 = tk.Entry(width=50)
    EditBox2.place(x=10, y=180)

    # Button = tk.Button(text=u'処理開始', width=50, command=sub_window)
    Button = tk.Button(text=u'処理開始', width=50, command=main)
    Button.place(x=10, y=220)

    root.mainloop()
