#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试local_cache模块的使用
"""

from utils.local_cache import local_data_cache, standardize_date
from datetime import datetime

@local_data_cache(update_frequency=1)
def fetch_test_data(start_date=None, end_date=None):
    """
    获取测试数据
    
    Args:
        start_date (str): 开始日期
        end_date (str): 结束日期
    
    Returns:
        dict: 日期为键，数据为值
    """
    if start_date is None:
        start_date = datetime.now().strftime('%Y%m%d')
    if end_date is None:
        end_date = datetime.now().strftime('%Y%m%d')
    
    # 标准化日期
    start = standardize_date(start_date)
    end = standardize_date(end_date)
    
    # 模拟获取数据
    print(f"正在获取从 {start} 到 {end} 的数据...")
    
    # 生成测试数据
    from utils.local_cache import generate_date_range
    result = {}
    for date in generate_date_range(start, end):
        result[date] = {
            "开盘价": 100 + float(date) % 10,
            "收盘价": 105 + float(date) % 15,
            "最高价": 110 + float(date) % 20,
            "最低价": 95 + float(date) % 5,
            "成交量": 10000 + float(date) % 5000
        }
    
    return result

if __name__ == "__main__":
    # 第一次调用会从网络获取数据
    data1 = fetch_test_data("20250101", "20250105")
    print(f"获取到 {len(data1)} 天的数据")
    
    # 第二次调用会使用缓存
    data2 = fetch_test_data("20250101", "20250105")
    print(f"从缓存获取到 {len(data2)} 天的数据")
    
    # 第三次调用部分使用缓存，部分重新获取
    data3 = fetch_test_data("20250103", "20250107")
    print(f"获取到 {len(data3)} 天的数据，部分来自缓存")
    
    print("测试完成!") 