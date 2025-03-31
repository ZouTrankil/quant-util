from utils import DataSource

pro = DataSource.tushare_pro


#查询当前所有正常上市交易的股票列表

data = pro.fina_indicator_vip(ts_code='000001.SZ')

data.to_csv('fina_indicator_vip.csv', index=False)
print(data)
