from utils import DataSource

pro = DataSource.tushare_pro


#查询当前所有正常上市交易的股票列表

data = pro.stock_basic(exchange='', list_status='L')

print(data)
