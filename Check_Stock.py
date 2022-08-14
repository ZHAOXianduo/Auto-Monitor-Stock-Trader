import requests
import json
import pandas as pd
from threading import Thread
import threading
import time
from urllib.parse import urlencode

### 导入股票列表
Stocks = pd.read_excel(r'监控清单.xlsx') # 获取股票代码
stock = Stocks['股票编码']

### 设置请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain',
    'Cookie': 'Hm_lvt_34e0d77f0c897023357dcfa7daa006f3=1647855686; __gads=ID=c25a642341619b6c-22dd524f12d1007a:T=1647855742:RT=1647855742:S=ALNI_Mbv_M5Jsav8E4b8U5FLdJei72eHig; yddxc=1; Hm_lpvt_34e0d77f0c897023357dcfa7daa006f3=1647859875',
    'Host': 'ddx.gubit.cn',
    'Referer': 'http://ddx.gubit.cn/drawddx.html'
}

### 设置抓取链接
URL_c = 'http://ddx.gubit.cn/ygetddxdata.php?'

### 设置线程全局锁
lock = threading.Lock()

def get_check(st):
    with lock:
        if len(str(st)) == 4:
            st = '00' + str(st)
        params_c = {
            'code': str(st),
            'm': '0.64746361949036'
        }
        r = requests.get(URL_c,params=params_c,verify=False,headers=HEADERS,timeout=4.0)
        data = r.text.split('<=>')[-1]
        for i in data.split('|'):
            print(i)
        print(st,r.status_code)
    return 0

# f11 买五价 f13 买四价 f15 买三价 f17 买二价 f19 买一价 f31 卖五价 f33 卖四价 f35 卖三价 f37 卖二价 f39 卖一价
# f12 买五量 f14 买四量 f16 买三量 f18 买二量 f20 买一量 f32 卖五量 f34 卖四量 f36 卖三量 f38 卖二量 f40 卖一量
# 最高 f44 最低 f45 当前交易量f47手（外盘f49） 当前交易额f48元 量比f50 当前换手率f168 主力流入f135 主力流出f136 主力净流入f137
# 超大单流入f138 超大单流出f139 超大单差额f140
# 大单流入f141 大单流出f142 大单差额f143
# 中单流入f144 中单流出f145 中单差额f146
# 小单流入f147 小单流出f148 小单差额f149
# 动态市盈率f162 总市值f116 流动市值f117

def thread_c():
    print(u'多线程抓取')
    ts = [Thread(target=get_check, args=(st,)) for st in stock]
    starttime= time.time()
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    endtime=time.time()
    print('总花费时间：',endtime-starttime)
    return 0