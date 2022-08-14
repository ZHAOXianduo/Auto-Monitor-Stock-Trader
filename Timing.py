## 此模块用来信息抓取的时间频率
### 价格数据——实时频率，依据数据抓取量设置频率
### 大宗交易——一天抽取一次
### 异常数据——一天抽取一次
### 基本面数据——一周更新一次的时候抓取一次

import datetime
import pandas as pd

now = datetime.datetime.now()
year_ = now.year
mon_ = now.month
day_ = now.day
open_1 = datetime.datetime.strptime(str(year_) + '-' + str(mon_) + '-' + str(day_) + ' ' + '09:15:00',"%Y-%m-%d %H:%M:%S")
close_1 = datetime.datetime.strptime(str(year_) + '-' + str(mon_) + '-' + str(day_) + ' ' + '11:30:00',"%Y-%m-%d %H:%M:%S")
open_2 = datetime.datetime.strptime(str(year_) + '-' + str(mon_) + '-' + str(day_) + ' ' + '11:48:00',"%Y-%m-%d %H:%M:%S")
close_2 = datetime.datetime.strptime(str(year_) + '-' + str(mon_) + '-' + str(day_) + ' ' + '22:10:00',"%Y-%m-%d %H:%M:%S")

def price_time(sec,tm):
    if (tm > open_1 and tm < close_1) or (tm > open_2 and tm < close_2):
        return 1,tm+datetime.timedelta(seconds=sec)
    elif tm > close_1 and tm < open_2:
        print('等开盘')
        return 1,open_2
    else:
        return 0,0
