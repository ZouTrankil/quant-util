#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/3/28.
@author: Air.Zou
"""

from utils.global_config import DataSource
from utils.code_symbol import code_symbol
import pandas as pd

def get_daily_data(code, start_date: str, end_date: str) -> pd.DataFrame:
    """
    获取指定股票代码在指定日期范围内的日线数据

    Args:
        code (str): 股票代码
        start_date (str): 开始日期
        end_date (str): 结束日期

    Returns:
        pd.DataFrame: 日线数据
    """
    pro = DataSource.tushare_pro
    code = code_symbol(code)
    stock = pro.daily(ts_code=code, start_date=start_date
                                         , end_date=end_date)

    stock.set_index('trade_date', inplace=True)
    stock.sort_index(inplace=True)
    return stock


if __name__ == "__main__":
    stock = get_daily_data('000001', '20250101', '20251231')
    print(stock)

    #提取000001全部复权因子
    # df = DataSource.tushare_pro.adj_factor(ts_code='000001.SZ', trade_date='')
    # print(df)
    # df = DataSource.tushare_pro.stk_factor_pro(ts_code='600059.SZ', start_date='20240328', end_date='20250328')
    # print(df)
    # df = DataSource.tushare_pro.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20251011')
    # print(df)
    #提取2018年7月18日复权因子
    # df = DataSource.tushare_pro.adj_factor(ts_code='', trade_date='20180718')
