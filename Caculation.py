def BS_ratio(ratio,record):
    if ratio == '-': ratio = 0
    if record == '-': record = 0
    ratio = float(ratio)
    record = float(record)
    if abs(ratio) > 10 and abs(record)<10:
        if ratio > 0:
            return ('出现极大极大买盘'+'量比为：'+str(ratio)) #alarm
        else:
            return ('出现极大极大卖盘'+'量比为：'+str(ratio)) #alarm
    return 0

def C_ratio(ratio,record):
    if ratio == '-': ratio = 0.00
    if record == '-': record = 0.00
    ratio = float(ratio)
    record = float(record)
    if ratio >= 1 and record < 1:
        return ('换手率增长，超过1%，当前换手率为：'+str(ratio)+'%')
    elif ratio >=5 and record < 5:
        return ('换手率增长，超过5%，当前换手率为：'+str(ratio)+'%')
    else:
        return 0

def inflow(inflow_,record):
    if inflow_ == '-': inflow_ = 0.00
    if record == '-': record = 0.00
    inflow_ = float(inflow_)
    record = float(record)
    print('净流入：',inflow_,record)
    if inflow_ > 0 and record <=0:
        return ('主力资金异动，主力净流入，当前流入：'+'￥'+str(inflow_/10000)+'万元')
    elif inflow_ < 0 and record >=0:
        return ('主力资金异动，主力净流出，当前流出：'+'￥'+str(-inflow_/10000)+'万元')
    else:
        return 0

def change_r(ratio,record):
    print(ratio, record)
    if ratio == '-': ratio = 0.00
    if record == '-': record = 0.00
    ratio = float(ratio)
    record = float(record)
    if  abs(ratio) > 3 and abs(record) < 3:
        if ratio > 0:
            return ('股价上涨超过3%，当前涨幅：'+str(ratio)+'%')
        else:
            return ('股价下跌超过3%，当前跌幅：'+str(ratio)+'%')
    elif abs(ratio) > 6 and abs(record) < 6:
        if ratio > 0:
            return ('股价上涨超过6%，当前涨幅：'+str(ratio)+'%')
        else:
            return ('股价下跌超过6%，当前跌幅：'+str(ratio)+'%')
    elif abs(ratio) > 9 and abs(record) < 9:
        if ratio > 0:
            return('股价上涨超过9%，当前涨幅：'+str(ratio)+'%')
        else:
            return('股价下跌超过9%，当前跌幅：'+str(ratio)+'%')

    if  abs(record) > 3 and abs(ratio) < 3:
        if ratio > 0:
            return ('股价涨幅收缩至小于3%，当前涨幅：'+str(ratio)+'%')
        else:
            return ('股价跌幅收缩至小于3%，当前跌幅：'+str(ratio)+'%')
    elif abs(record) > 6 and abs(ratio) < 6:
        if ratio > 0:
            return ('股价涨幅收缩至小于6%，当前涨幅：'+str(ratio)+'%')
        else:
            return ('股价跌幅收缩至小于6%，当前跌幅：'+str(ratio)+'%')
    elif abs(record) > 9 and abs(ratio) < 9:
        if ratio > 0:
            return('股价涨幅收缩至小于9%，当前涨幅：'+str(ratio)+'%')
        else:
            return('股价跌幅收缩至小于9%，当前跌幅：'+str(ratio)+'%')
    else:
        return 0