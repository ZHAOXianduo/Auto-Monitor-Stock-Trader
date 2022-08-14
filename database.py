import pymysql

def SQL_(record,node):
    # 打开数据库连接
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='ZXDhelin030@',
                         database='TESTDB',
                         charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 插入
    cursor.execute("select database();")
    # 关闭数据库连接
    db.close()
    return 0

#mysql> create table if not exists mass_trade(
#    -> 编码 varchar(6) not null,
#    -> 交易日期 varchar(10) not null,
#    -> 涨跌幅 float,
#    -> 收盘价 float,
#    -> 成交价 float,
#    -> 折溢率 float,
#    -> 成交量 float,
#    -> 成交额（万元） float,
#    -> 成交额占流通市值 float,
#    -> 买方营业部 text,
#    -> 卖方营业部 text,
#    -> 1日后涨跌幅 float,
#    -> 5日后涨跌幅 float,
#    -> 10日后涨跌幅 float,
#    -> 20日后涨跌幅 float
#    -> );







# 使用 fetchone() 方法获取单条数据.)YeM/:IlI4h7
#data = cursor.fetchone()


