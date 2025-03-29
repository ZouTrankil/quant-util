#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 16/03/2025.
@author: Air.Zou
"""
from utils.date_utils import get_days_ago, get_current_date_str
from utils.global_config import DataSource
import akshare as ak

pro = DataSource.tushare_pro

#
# def index_basic():
#     return pro.index_basic(market='CSI')
#
#
# def get_index_constituents(index_code='000300.SH', days=5):
#     start = get_days_ago(days=days)
#     end = get_current_date_str()
#     print(start, end)
#     index_weight = pro.index_weight(index_code=index_code, start_date=start, end_date=end)
#     return index_weight

# https://www.csindex.com.cn/zh-CN/indices/index-detail/931059#/
# csi 中证指数
A500 = '000510' # 中证A500指数代码
ZZ500 = '000905' # 中证500 小盘指数代码
ETF300 = '000300' # 沪深300指数代码
A50 = '930050' # A50指数代码
ZZHL100 = '000922' # ZZ红利100指数代码

def hs300_constituents():
    return ak.index_stock_cons_csindex(symbol=ETF300)

def a500_constituents():
    return ak.index_stock_cons_csindex(symbol=A500)

def a50_constituents():
    return ak.index_stock_cons_csindex(symbol=A50)

if __name__ == '__main__':
    print("hs300_constituents")
    print(hs300_constituents())
    print("a500_constituents")
    print(a500_constituents())
    print("a50_constituents")
    print(a50_constituents())