# 此模块用于抓取一天的价格异动

### 导入所需的数据库
import requests
import json
import pandas as pd
from threading import Thread
import threading
import time
from urllib.parse import urlencode
from cleaning_ab import cleaning_ab

### 导入股票列表
Stocks = pd.read_excel(r'监控清单.xlsx') # 获取股票代码
stock = Stocks['股票编码']

### 设置请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'Cookie': 'qgqp_b_id=d4c7d95b9a3fea432b6afb4394d1e7cb; em_hq_fls=js; cowCookie=true; st_si=11660912221455; cowminicookie=true; st_asi=delete; HAList=a-sz-301179-N%u6CFD%u5B87%2Cf-0-000012-%u56FD%u503A%u6307%u6570; intellpositionL=1215.35px; intellpositionT=955px; st_pvi=54890317298070; st_sp=2021-02-13%2023%3A08%3A33; st_inirUrl=https%3A%2F%2Fwww.sogou.com%2Flink; st_sn=12; st_psi=2021120911112711-113300300815-1187412359'
}

### 设置抓取链接
URL_ab = 'http://push2ex.eastmoney.com/getStockChanges?'

### 设置线程全局锁
lock = threading.Lock()

def get_ab(st,date):
    with lock:
        params_kl = {
            'ut': '7eea3edcaed734bea9cbfc24409ed989',
            'date': date,#修改以获取对应天数的板块异动
            'dpt': 'wzchanges',
            'market': str(int(str(st)[0] == '6')),
            'code': str(st),
            'cb': 'jQuery3510879963813839171_1647328941462',
            '_': str(round(time.mktime(time.localtime()))) #表示当前更新时间数据
        }
        r = requests.get(URL_ab + urlencode(params_kl),params=params_kl,verify=False,headers=HEADERS,timeout=2.0)
        Length = len(params_kl['cb'])
        data = json.loads('['+r.text[Length+1:-2]+']')[0]['data']['data']
        print(st,'Status:',r.status_code)
        print(data)
        cleaning_ab(data)
    return 0

def thread_ab():
    print(u'多线程抓取')
    now = time.localtime()
    year = now.tm_year
    mon = now.tm_mon
    day = now.tm_mday
    if mon < 10: mon = '0'+str(mon)
    if day < 10: day = '0'+str(day)
    date = str(year)+str(mon)+str(day)
    ts = [Thread(target=get_ab, args=(st,date)) for st in stock]
    starttime= time.time()
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    endtime=time.time()
    print('总花费时间：',endtime-starttime)
    return ts
