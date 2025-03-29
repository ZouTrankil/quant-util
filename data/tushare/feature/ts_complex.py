# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/3/28.
@author: Air.Zou
"""


from utils.global_config import DataSource
from utils.local_cache import local_data_cache


@local_data_cache(update_frequency=1)
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

