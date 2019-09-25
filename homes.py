from selenium import webdriver
import time


if __name__ == '__main__':
    url = "https://www.homes.co.jp/"
    # js対応
    # 1.操作するブラウザを開く
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options='')
    # 2.操作するページを開く
    driver.get(url)
    driver.add_cookie(
        {
            'TS018f23e9':
                '01c857bb1ccc7b80b8ce6db0b8fc8e8240f33f31163755c46ba520fe188a6ec7528b0e92068d0d9e244ca96413f4dc18e9b8ae7357b7978093c299822228b2884b400ab6aa',
            '_atrk_sessidx': '_atrk_sessidx',
            '_atrk_ssid': '9Eoe-Be5AKa4MC_j5ERiD9',
            '_fbp': 'fb.2.1566971644864.1375720806',
            '_gid': 'GA1.3.368561724.1567536559',
            '_ra': '1566971644873|45077cb1-1d10-4915-bc71-e6da2f9ddc8d',
            'appier_utmz': '%7B%22csr%22%3A%22www.homes.co.jp%22%2C%22timestamp%22%3A1566971689%2C%22lcsr%22%3A%22www.homes.co.jp%22%7D',
            'cX_S': 'k048wy1d3xub5w66',
            'cstp': '1',
            'cto_lwid': 'a367379e-7987-474e-81d7-0205b0e234d8',
            'krt.vis': '6ff9d5af-352d-4fe4-b913-c357c4196b27',
         })
    driver.find_element_by_tag_name('#prg-searchTypeList > '
                                    'div > '
                                    'ul.searchList > '
                                    'li.searchListItem.realtor > '
                                    'a').click()
    driver.find_element_by_tag_name('#prg-modalRealtor > '
                                    'div.modalContents > '
                                    'div > '
                                    'div > '
                                    'div > '
                                    'ul:nth-child(1) > '
                                    'li > a > span').click()
    # chromeDriver の終了
    # driver.quit()
