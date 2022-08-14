### 导入股票列表
import pandas as pd
import Caculation as CL
import threading
### 设置线程全局锁
lock = threading.Lock()
pd.set_option('mode.chained_assignment', None)

Stocks = pd.read_excel(r'实时清单.xlsx', index_col='股票编码')  # 获取股票代码
Stocks['主力净流入'] = Stocks['主力净流入'].astype('float')
Stocks['量比'] = Stocks['量比'].astype('float')
Stocks['换手率'] = Stocks['换手率'].astype('float')
Stocks['涨跌幅'] = Stocks['涨跌幅'].astype('float')

def cleaning_p(data):
    with lock:
        print(Stocks)
        Mail = []
        stock = Stocks[Stocks.index == int(data['f57'])]
        BS = CL.BS_ratio(data['f50'], stock['量比'][int(data['f57'])])
        if BS != 0: Mail.append(BS)
        Stocks['量比'][int(data['f57'])] = data['f50']

        C_r = CL.C_ratio(data['f168'], stock['换手率'][int(data['f57'])])
        if C_r != 0: Mail.append(C_r)
        Stocks['换手率'][int(data['f57'])] = data['f168']

        net = CL.inflow(data['f137'], stock['主力净流入'][int(data['f57'])])
        if net != 0: Mail.append(net)
        Stocks['主力净流入'][int(data['f57'])] = data['f137']

        change = CL.change_r(data['f170'], stock['涨跌幅'][int(data['f57'])])
        if change != 0: Mail.append(change)
        Stocks['涨跌幅'][int(data['f57'])] = data['f170']

        writer = pd.ExcelWriter('实时清单.xlsx')
        Stocks.to_excel(writer, float_format='%.5f')
        writer.save()

    print(Stocks)

    return Mail,str(data['f57'])

# f57 股票编码 F58 股票名称
# f11 买五价 f13 买四价 f15 买三价 f17 买二价 f19 买一价 f31 卖五价 f33 卖四价 f35 卖三价 f37 卖二价 f39 卖一价
# f12 买五量 f14 买四量 f16 买三量 f18 买二量 f20 买一量 f32 卖五量 f34 卖四量 f36 卖三量 f38 卖二量 f40 卖一量
# 最高 f44 最低 f45 当前交易量f47手（外盘f49） 当前交易额f48元 量比f50 当前换手率f168 主力流入f135 主力流出f136 主力净流入f137
# 超大单流入f138 超大单流出f139 超大单差额f140
# 大单流入f141 大单流出f142 大单差额f143
# 中单流入f144 中单流出f145 中单差额f146
# 小单流入f147 小单流出f148 小单差额f149
# 动态市盈率f162 总市值f116 流动市值f117

#  关注量比：正负号变动/极大买盘卖盘，日内异常买盘卖盘波动，历史异常买盘卖盘波动
#  换手率：1%为门槛，5%为门槛，10%为门槛，20%为门槛
#  交易量：主力净流入正负号变动，大额交易单占比，主力净流入占买盘
#  实时数据库更新
#  股价上涨变化警示：日内新高，日内新低，涨跌幅3%，涨跌幅9%