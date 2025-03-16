#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/03/2025.
@author: Air.Zou
"""

import datetime


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

if __name__ == '__main__':
    print(get_current_date_str())
    print(get_days_ago(2))
