# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import tushare as ts

from utils.global_config import DataSource
from utils.local_cache import every_day_update, permenant_cache


## 获取所有股票基本信息

@permenant_cache()
def get_stock_all_basic():
    pro = DataSource.tushare_pro
    data = pro.stock_basic(exchange='', list_status='L')
    return data


@permenant_cache()
def get_stock_all_out():
    pro = DataSource.tushare_pro
    data = pro.stock_basic(exchange='', list_status='D')
    return data

#获取沪股通成分
@permenant_cache()
def get_stock_hshk():
    pro = DataSource.tushare_pro
    return pro.hs_const(hs_type='SH')

@permenant_cache()
def get_stock_szhk():
    pro = DataSource.tushare_pro
    return pro.hs_const(hs_type='SZ')

if __name__ == '__main__':
    print(get_stock_all_basic())
    print(get_stock_all_out())
    print(get_stock_hshk())
    print(get_stock_szhk())

