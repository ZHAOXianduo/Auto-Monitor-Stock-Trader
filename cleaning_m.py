import datetime
import database as db

now =  datetime.datetime.now()

def recording(table,node):
    for i in table:
        record_t = datetime.datetime.strptime(i[1],"%Y-%m-%d")
        if (now-record_t).days < 10:
            db.SQL_(node,i)
    return 0


def filter(table,url):
    o_t_t = datetime.datetime.strptime(table[-1].split(' ')[1],"%Y-%m-%d")
    if (now-o_t_t).days < 10 and len(table) == 50:
        recording(table,url[-11:-5])
        return  101
    else:
        recording(table,url[-11:-5])
        return 0
        #for record in table: print(record)

# 如果当前页的信息不完全囊括过去七天大宗交易，相应爬虫函数翻页继续抽取数据--只是做了初步解决
# 数据清洗脚本需要做基础的统计分析
# 每一条记录的实际含义如下：
## 1.序号
## 2.交易日期
## 3.涨跌幅（%）
## 4.收盘价
## 5.成交价
## 6.折溢率
## 7.成交量
## 8.成交额（万元）
## 9.成交额/流通市值
## 10.买方营业部
## 11.卖方营业部
## 12.上榜后1日涨跌幅（%）
## 13.上榜后5日涨跌幅（%）
## 14.上榜后10日涨跌幅（%）
## 15.上榜后20日涨跌幅（%）