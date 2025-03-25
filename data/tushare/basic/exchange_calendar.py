#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/03/2025.
@author: Air.Zou
"""
from typing import List

from utils.date_utils import get_current_date_str
from utils.global_config import DataSource


def get_trade_days_info(start_date:str = None, end_date:str = None):
    if end_date is None:
        end_date = get_current_date_str()
    return DataSource.tushare_pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)

def get_trade_days_str(start_date:str = None, end_date:str = None) -> List[str]:
    if end_date is None:
        end_date = get_current_date_str()
    result = DataSource.tushare_pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)
    list_result = result[result['is_open'] == 1]['cal_date'].tolist()
    # sort list_result
    list_result.sort()
    return list_result

if __name__ == '__main__':
    print(get_trade_days_str())
    # print(get_trade_days_info())

# result
#       exchange  cal_date  is_open pretrade_date
# 0          SSE  20251231        1      20251230
# 1          SSE  20251230        1      20251229
# 2          SSE  20251229        1      20251226
#