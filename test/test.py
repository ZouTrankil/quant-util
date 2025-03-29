from utils import DataSource

pro = DataSource.tushare_pro

df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')

print(df)
