def cleaning_ab(data):
    if len(data) == 0:
        return 0
    else:
        for i in data:
            print(i)
        print("Abnormal records")

# 'tm' 交易时间 小时，分钟，秒数
# 'i' 交易手数/如果小于1则是股价异常波动
# 'p' 交易价格*1000
# 'v' 成交量
# 't' 异常类型：64-大买盘，128-大卖盘，8204-加速下跌，8203-高台跳水，8201-火箭发射，8215-60日大幅上涨
# 'u' 相应涨跌幅