# https://suumo.jp/kaisha/nagano/sc_kitasakugun/
import urllib.request as u
from bs4 import BeautifulSoup
import time
import re
import csv


def soup(url):
    res = u.urlopen(url)
    soup = BeautifulSoup(res, 'html.parser', from_encoding='UTF-8')
    return soup


def getEstateURLS(soup_data):
    dataURLS = soup_data.select('div.cassettebox-title > h2 > a')
    urls = [i.get('href') for i in dataURLS]
    return urls


def url_join(urls):
    joinUrls = [u.urljoin('https://suumo.jp/', i) for i in urls]
    return joinUrls


def cleanhtml(raw_html):
    cleanr = re.compile(r"<[^>]*?>")
    cleantext = cleanr.sub('', raw_html)
    return cleantext


def getData(join_urlList):
    dataList = []
    for u in join_urlList:
        op = soup(u)
        name = op.select_one('h1').get_text()
        print(u)
        adrres = op.select_one('div.mt20 > table > tbody > tr:nth-child(1) > td')
        if adrres is None:
            com = op.select('table.data_table.table_gaiyou > tr > td')
            adrres = com[0].get_text()
            tel = op.select_one('.fs-big').get_text().replace('\n', '')
            fax = com[3].get_text()
            companyUrl = str(com[6]).replace("'", '"')\
                .replace('<td>', '').replace('<a href="javascript:void(0);" onclick="javascript:popUpMap2("', '')\
                .replace('", "01"); return false;">', '')\
                .replace('当社ＨＰはこちら', '')\
                .replace('<br>', '')\
                .replace('</a>', '')\
                .replace('</br>', '')\
                .replace('</td>', '')\
                .replace('!', '').replace('当社HPはこちら！', '').replace('\n', '').replace('-', '').replace('当社ホームページへ', '')
            print(companyUrl)
        else:
            adrres = adrres.get_text()
            tel = op.select_one('div.mt20 > table > tbody > tr:nth-child(2) > td:nth-child(2) > div:nth-child(1) > em > span.fs18').get_text()
            fax = op.select_one('div.mt20 > table > tbody > tr:nth-child(2) > td:nth-child(4)').get_text()
            companyUrl = op.select_one('div.mt20 > table > tbody > tr:nth-child(4) > td > ul > li:nth-child(1) > a')
            if companyUrl is None:
                companyUrl = "-"
            else:
                companyUrl = companyUrl.get('href')
        dataList.append([name, adrres, tel, fax, companyUrl])
        time.sleep(1)
    return dataList


if __name__ == '__main__':
    # url = "https://suumo.jp/kaisha/nagano/sc_kitasakugun/" # 長野県　北佐久郡
    # url = "https://suumo.jp/kaisha/nagano/sc_chino/" # 長野県　茅野市
    # url = 'https://suumo.jp/kaisha/hyogo/sc_kobeshikita/' # 兵庫県神戸市北区
    # url = 'https://suumo.jp/kaisha/hyogo/sc_toyooka/' # 兵庫県豊岡市
    # url = 'https://suumo.jp/kaisha/kagoshima/sc_kirishima/' # 鹿児島県霧島市
    # url = 'https://suumo.jp/kaisha/oita/sc_hita/' # 大分県日田市
    # url = 'https://suumo.jp/kaisha/hokkaido_/sc_noboribetsu/' # 北海道登別市	北海道	登別市
    url = "https://suumo.jp/kaisha/kagawa/sc_takamatsu/" # 香川県高松市

    soupData = soup(url)
    urlList = getEstateURLS(soupData)
    data = getData(url_join(urlList))
    with open('suumo_kagawaken_takamatusi.csv', 'a', newline='', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)
