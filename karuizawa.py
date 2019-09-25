# -* UTF-8 Python3.6 *-
import urllib.request as u
from bs4 import BeautifulSoup
import time
import re
import pandas as pd

def soup(url):
    res = u.urlopen(url)
    soup_data = BeautifulSoup(res, 'html.parser', from_encoding='UTF-8')
    return soup_data


def get_estate_urls(soup_data):
    data = soup_data.select('#search-body > a')
    urls = [i.get('href') for i in data]
    return urls


def url_join(urls):
    join_urls = [u.urljoin('https://www.royal-resort.co.jp/', i) for i in urls]
    return join_urls


def clean_html(raw_html):
    clean_r = re.compile(r"<[^>]*?>")
    clean_text = clean_r.sub('', raw_html)
    return clean_text


def main(url):
    """　メイン処理を実行　"""
    soup_data = soup(url)
    url_list = get_estate_urls(soup_data)
    tempo_urls = url_join(url_list)
    to_csv = []
    for z in tempo_urls:
        perser_data = soup(z)
        name = perser_data.select_one('#totop > div.main-container > '
                                      'section:nth-child(3) > '
                                      'div.pg-detail-head > h3')
        if name is None:
            name = "-"
        else:
            name = name.get_text().strip(' ').strip('\n').replace(' ', '').replace('\u3000', '')


        sub_title = perser_data.select_one('#totop > div.main-container > '
                                           'section:nth-child(3) > '
                                           'div.pg-detail-head > p')
        if sub_title is None:
            sub_title = "-"
        else:
            sub_title = sub_title.get_text().strip(' ').strip('\n').replace(' ', '')


        point = [i.get_text().replace(' ', '').replace('\n', ' ').replace('\xa01', '')
                 for i in perser_data.select('#totop > div.main-container > section:nth-child(3) > '
                                             'div.pg-detail-first > div.pg-detail-first-side')]


        detail = [i.get_text().replace('\xa01', '').replace('\u3000', '').replace(' ', '')
                      .replace('\n\n\n', ' ').replace('\n', '')
                 for i in perser_data.select('#totop > div.main-container > section:nth-child(3) > '
                                             'div.pg-detail-etc-wrapper > div:nth-child(1)')]


        onsen = perser_data.select_one('#totop > div.main-container > section:nth-child(3) > '
                                       'div.pg-detail-etc-wrapper > div:nth-child(2) > '
                                       'table:nth-child(2) > tbody > tr > td')
        if onsen is None:
            onsen = "-"
        else:
            onsen = onsen.get_text().replace(' ', '').strip('\n')


        biko = perser_data.select_one('#totop > div.main-container > section:nth-child(3) > div.pg-detail-etc-wrapper > '
                                      'div:nth-child(2) > table:nth-child(4)')
        if biko is None:
            biko = "-"
        else:
            biko = biko.get_text().replace(' ', '').replace('\n', '').replace('\u3000', '')


        tel = perser_data.select_one('#totop > div.main-container > '
                                     'section:nth-child(3) > div.pg-detail-contact > p')
        if tel is None:
            tel = "-"
        else:
            tel = tel.get_text().replace('\n', '').replace(' ', '')


        from_seller = perser_data.select_one('#totop > div.main-container > section:nth-child(3) > '
                                             'div.pg-detail-drawing-wrapper > div.pg-voice-wrapper > '
                                             'dl:nth-child(1)')
        if from_seller is None:
            from_seller = "-"
        else:
            from_seller = from_seller.get_text().replace(' ', '').replace('\n', '').replace('売主様より', '(売主様より)')


        from_tanto = perser_data.select_one('#totop > div.main-container > section:nth-child(3) > '
                                            'div.pg-detail-drawing-wrapper > div.pg-voice-wrapper > '
                                            'dl:nth-child(2)')
        if from_tanto is None:
            from_tanto = "-"
        else:
            from_tanto = from_tanto.get_text().replace(' ', '').replace('\n', '').replace('担当者より', '(担当者より)')


        drive = perser_data.select_one('#totop > div.main-container > section:nth-child(3) > '
                                       'div.pg-detail-office-wrapper > div > dl:nth-child(1) > '
                                       'dt.pg-detail-office-info__txt')
        if drive is None:
            drive = "-"
        else:
            drive = drive.get_text().replace(' ', '').strip('\n')


        address = perser_data.select_one('#totop > div.main-container > section:nth-child(3) > '
                                         'div.pg-detail-office-wrapper > div > dl:nth-child(2) > '
                                         'dt.pg-detail-office-info__txt')
        if address is None:
            address = "-"
        else:
            address = address.get_text().replace(' ', '').strip('\n')
        to_csv.append([name, sub_title, point, detail, onsen, biko, tel, from_seller, from_tanto, drive, address])
        time.sleep(1)
    return to_csv


if __name__ == '__main__':
    urls = [ "https://www.royal-resort.co.jp/karuizawa/estate_list_karuizawa/sell/" \
          "?page=" + str(i)+ "&keyword=&sort=&direction=&p_limit=&sale_type_str=sell" \
          "&area_roma=karuizawa&feature=&kind_code=2&price" for i in range(1, 14)]
    for f, i in enumerate(urls):
        to_csv = main(i)
        print(to_csv)
        df = pd.DataFrame(to_csv)
        df.to_csv('kanazawa_'+ str(f) +'.csv',
                  header=['名前', 'サブタイトル', 'ポイント', '詳細', '温泉', '備考', '電話番号', '売主より', '担当者より', '交通', '所在地'],
                  index=False,
                  encoding='UTF-8')
        time.sleep(1)
