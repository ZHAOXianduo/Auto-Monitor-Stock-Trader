## 为了加快抓取速度，抓取模块采用的是较为底层的requests包
## 并发并行采用的是多线程并行处理I/O密集型任务
## 当前版本1.0
## 版本日志：
## 新建 1.0版本 2022年3月15日 实现功能：实时抓取个股价格，涨跌幅，涨跌价格，交易量

### 导入所需的数据库
import requests
import json
import pandas as pd
from threading import Thread
import threading
import time
from urllib.parse import urlencode
from cleaning_p import cleaning_p

### 导入股票列表
Stocks = pd.read_excel(r'监控清单.xlsx') # 获取股票代码
stock = Stocks['股票编码']

### 设置请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'Cookie': 'qgqp_b_id=d4c7d95b9a3fea432b6afb4394d1e7cb; em_hq_fls=js; cowCookie=true; st_si=11660912221455; cowminicookie=true; st_asi=delete; HAList=a-sz-301179-N%u6CFD%u5B87%2Cf-0-000012-%u56FD%u503A%u6307%u6570; intellpositionL=1215.35px; intellpositionT=955px; st_pvi=54890317298070; st_sp=2021-02-13%2023%3A08%3A33; st_inirUrl=https%3A%2F%2Fwww.sogou.com%2Flink; st_sn=12; st_psi=2021120911112711-113300300815-1187412359'
}

### 设置抓取链接
URL_p = 'http://push2.eastmoney.com/api/qt/stock/get?'

### 设置线程全局锁
lock = threading.Lock()

def get_price(st,Mails):
    with lock:
        if len(str(st)) == 4:
            st = '00' + str(st)
        params_kl = {
            'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
            'invt': '2',
            'fltt': '2',
            'fields': 'f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f163,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f530,f135,f136,f137,f138,f139,f141,f142,f144,f145,f147,f148,f140,f143,f146,f149,f55,f62,f162,f92,f173,f104,f105,f84,f85,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f107,f111,f86,f177,f78,f110,f262,f263,f264,f267,f268,f250,f251,f252,f253,f254,f255,f256,f257,f258,f266,f269,f270,f271,f273,f274,f275,f127,f199,f128,f193,f196,f194,f195,f197,f80,f280,f281,f282,f284,f285,f286,f287,f292',
            'secid': str(int(str(st)[0] == '6')) + '.' + str(st),
            'cb': 'jQuery1124006513137063565533_1647239726317',
            '_': str(round(time.mktime(time.localtime()))) #表示当前更新时间数据
        }
        r = requests.get(URL_p + urlencode(params_kl),params=params_kl,verify=False,headers=HEADERS,timeout=3.0)
        Length = len(params_kl['cb'])
        data = json.loads('['+r.text[Length+1:-2]+']')[0]['data']
        print(st,data['f58'],'Status:',r.status_code)
        print('当前价格：','￥',data['f43'])
        #print('当前涨跌额：','￥',data['f169'])
        print('当前涨跌幅：','￥',data['f170'],'%')
        mail,notation = cleaning_p(data)
        if len(mail) > 0:
            Mails.append(notation+' '+data['f58']+':')
            Mails.extend(mail)
            Mails.append('当前价格：'+str(data['f43']))
    return 0

# f11 买五价 f13 买四价 f15 买三价 f17 买二价 f19 买一价 f31 卖五价 f33 卖四价 f35 卖三价 f37 卖二价 f39 卖一价
# f12 买五量 f14 买四量 f16 买三量 f18 买二量 f20 买一量 f32 卖五量 f34 卖四量 f36 卖三量 f38 卖二量 f40 卖一量
# 最高 f44 最低 f45 当前交易量f47手（外盘f49） 当前交易额f48元 量比f50 当前换手率f168 主力流入f135 主力流出f136 主力净流入f137
# 超大单流入f138 超大单流出f139 超大单差额f140
# 大单流入f141 大单流出f142 大单差额f143
# 中单流入f144 中单流出f145 中单差额f146
# 小单流入f147 小单流出f148 小单差额f149
# 动态市盈率f162 总市值f116 流动市值f117

def thread_p(Mails):
    print(u'多线程抓取')
    ts = [Thread(target=get_price, args=(st,Mails)) for st in stock]
    starttime= time.time()
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    endtime=time.time()
    print('总花费时间：',endtime-starttime)
    print(len(Mails))
    return Mails

