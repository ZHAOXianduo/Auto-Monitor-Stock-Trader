#此模块负责抓取大宗交易，一天一抓

from selenium import webdriver
from cleaning_m import filter
from threading import Thread
import threading
import time
import pandas as pd

### 导入股票列表
Stocks = pd.read_excel(r'监控清单.xlsx') # 获取股票代码
Stocks['股票编码'] = Stocks['股票编码'].astype(str)
for i in range(len(Stocks)):
    if len((Stocks['股票编码'][i])) == 4:
        Stocks['股票编码'][i] = '00'+str(Stocks['股票编码'][i])

URLs = [f"https://data.eastmoney.com/dzjy/detail/{str(stock)}.html"
        for stock in Stocks['股票编码']
        ]

lock = threading.Lock()

def page(browser,n,url):
    browser.find_element_by_class_name('ipt').clear()
    browser.find_element_by_class_name('ipt').send_keys(str(n))
    browser.find_element_by_class_name('btn').click()
    table = browser.find_element_by_class_name('dataview-body')
    turn = filter(table.text.split('\n')[24:],url)  # 翻页问题需要解决
    if turn == 101:
        page(browser,n+1,url)
    return 0


def auto_m(url,browser):
    with lock:
        browser.get(url)
        table = browser.find_element_by_class_name('dataview-body')
        turn = filter(table.text.split('\n')[24:],url) #翻页问题需要解决
        if turn == 101:
            page(browser,2,url)
            return 0
    return 0

def thread_m():
    print(u'多线程抓取')
    browser = webdriver.Chrome()
    ts = [Thread(target=auto_m, args=(url,browser)) for url in URLs]
    starttime= time.time()
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    endtime=time.time()
    print('总花费时间：',endtime-starttime)
    browser.close()
    return ts


