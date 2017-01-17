# coding: UTF-8
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import sys

def get_info(response):
    hydm = []
    hymc = []
    shzb_num = []
    shzb_avg = []
    zxqy_num = []
    zxqy_avg = []
    cy_num = []
    cy_avg = []
    sz_num = []
    sz_avg = []

    response.encoding = 'GBK'
    html = response.text
    print html

    soup = BeautifulSoup(html, 'html.parser')
    arcicle = soup.find('table', {'class': 'cls-data-table-common cls-data-table'})
    tr=arcicle.find_all('tr')

    if len(tr)-1>2:
        for i in range(2, len(tr)):
            td=tr[i].find_all('td')
            hydm.append(td[0].string.strip())
            hymc.append(td[1].string.strip())
            shzb_num.append(td[2].string.strip())
            shzb_avg.append(td[3].string.strip())
            zxqy_num.append(td[4].string.strip())
            zxqy_avg.append(td[5].string.strip())
            cy_num.append(td[6].string.strip())
            cy_avg.append(td[7].string.strip())
            sz_num.append(td[8].string.strip())
            sz_avg.append(td[9].string.strip())

        df=DataFrame(hydm, columns=['hydm'])
        df['hymc']=DataFrame(hymc)
        df['shzb_num']=DataFrame(shzb_num)
        df['shzb_avg']=DataFrame(shzb_avg)
        df['zxqy_num']=DataFrame(zxqy_num)
        df['zxqy_avg']=DataFrame(zxqy_avg)
        df['cy_num']=DataFrame(cy_num)
        df['cy_avg']=DataFrame(cy_avg)
        df['sz_num']=DataFrame(sz_num)
        df['sz_avg']=DataFrame(sz_avg)
        return df
    else:
        return None

if __name__ == '__main__':

    url = 'http://www.szse.cn/szseWeb/FrontController.szse'

    headers = {
        'Host': 'www.szse.cn',
        'Content-Length': '97',
        'Origin': 'http://www.szse.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'charset': 'UTF-8',
        'Accept': '*/*',
        'Referer': 'http://www.szse.cn/main/marketdata/tjsj/hysyl/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh',
        'q': '0.8'
    }

    for i in range(1, 12):
        for j in range(1, 30):
                data = 'ACTIONID=7&AJAX=AJAX-TRUE&CATALOGID=1794&TABKEY=tab1&REPORT_ACTION=search&txtQueryDate=2016-' + str(i) + '-' + str(j)
                data = requests.post(url, data=data, headers=headers)
                # print data
                page = get_info(data)

                print type(page)

                if page is None:
                    continue
                else:
                    name = '2016-' + str(i) + '-' + str(j) + '.csv'
                    # f = open(name, 'w+')
                    page.to_csv('data/' + name, encoding='GBK', index=False)
