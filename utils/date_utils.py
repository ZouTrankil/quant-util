#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/03/2025.
@author: Air.Zou
"""

import datetime
from typing import List, Tuple

def judge_weekend(current_date):
    weekday = current_date.weekday()
    return weekday == 5 or weekday == 6

# 排除星期6和星期7
def get_current_none_weekend_date_str():
    current_date = datetime.date.today()
    weekday = current_date.weekday()

    # 排除周末
    if weekday == 5:  # 星期六
        current_date -= datetime.timedelta(days=1)
    elif weekday == 6:  # 星期日
        current_date -= datetime.timedelta(days=2)

    formatted_date = current_date.strftime("%Y%m%d")
    return formatted_date

def get_current_date_str():
    current_date = datetime.date.today()
    formatted_date = current_date.strftime("%Y%m%d")
    return formatted_date

def get_days_ago(days):
    # 获取当前日期
    current_date = datetime.date.today()
    # 计算 days 天前的日期
    days_ago_date = current_date - datetime.timedelta(days=days)
    # 将日期转换为字符串
    formatted_date = days_ago_date.strftime("%Y%m%d")
    return formatted_date

def get_exchange_days(start_date, end_date) -> (str, str):
    return start_date, end_date

def get_increment_days(local_date=None, start_date='19900309', end_date=None) -> List[str]:
    # 本地有一系列数据，localDate = ['20230309', '20230310', '20230311', '20230312']
    # 从start_date开始，到end_date结束，返回不在localDate中的日期
    if local_date is None:
        local_date = []
    if end_date is None:
        end_date = get_current_date_str()

    start = datetime.datetime.strptime(start_date, "%Y%m%d").date()
    end = datetime.datetime.strptime(end_date, "%Y%m%d").date()
    local_set = set(local_date)
    result = []
    current = start
    while current <= end:
        date_str = current.strftime("%Y%m%d")
        if date_str not in local_set:
            if not judge_weekend(current):
                result.append(date_str)
        current += datetime.timedelta(days=1)

    return result

def some_func_1(start_date, end_date, increment:True):
    if end_date is None:
        end_date = get_current_none_weekend_date_str()
    return []

if __name__ == '__main__':
    print(get_current_date_str())
    print(get_days_ago(2))
    print(get_current_none_weekend_date_str())