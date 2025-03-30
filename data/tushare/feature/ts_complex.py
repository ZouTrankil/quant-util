# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/3/28.
@author: Air.Zou
"""
from utils.global_config import DataSource
from utils.local_cache import date_range_cache_with_symbol
from utils.log_util import logger
from utils.rate_limit_request import rate_limit

@rate_limit(28)
@date_range_cache_with_symbol(symbol_key='ts_code')
def stk_factor_pro_data(code, start_date, end_date):
    """
    获取指定股票代码在指定日期范围内的复权因子数据

    Args:
        code (str): 股票代码
        start_date (str): 开始日期
        end_date (str): 结束日期

    Returns:
        pd.DataFrame: 带复权带技术指标的日线数据
    """
    return DataSource.tushare_pro.stk_factor_pro(ts_code=code, start_date=start_date, end_date=end_date)


if __name__ == "__main__":
    df = stk_factor_pro_data(code='000001.SZ', start_date='20240328', end_date='20250328')
    print(df)
