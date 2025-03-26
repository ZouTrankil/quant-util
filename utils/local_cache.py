#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/03/2025.
@author: Air.Zou
"""
import os
import json
from functools import wraps
from datetime import datetime
from date_utils import get_current_none_weekend_date_str

def date_range_checker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 获取函数的参数名
        func_params = func.__code__.co_varnames[:func.__code__.co_argcount]

        # 将位置参数和关键字参数合并到一个字典中
        all_args = dict(zip(func_params, args))
        all_args.update(kwargs)

        # 获取start_date和end_date，如果没有提供则使用默认值
        start_date = all_args.get('start_date', datetime.now().strftime('%Y%m%d'))
        end_date = all_args.get('end_date')

        if end_date is None:
            end_date = get_current_none_weekend_date_str()

        # 确保日期格式正确
        start_date = standardize_date(start_date)
        end_date = standardize_date(end_date)

        # 构造文件名
        file_name = f"{func.__name__}_{start_date}_{end_date}.json"

        # 检查文件是否存在
        if os.path.exists(file_name):
            # 如果文件存在，读取本地数据
            with open(file_name, 'r') as f:
                return json.load(f)
        else:
            # 如果文件不存在，调用原函数获取网络数据
            result = func(**all_args)

            # 将结果保存到本地文件
            with open(file_name, 'w') as f:
                json.dump(result, f)

            return result

    return wrapper

def standardize_date(date_str):
    """
    标准化日期字符串为'YYYYMMDD'格式
    """
    if isinstance(date_str, str):
        try:
            date = datetime.strptime(date_str, '%Y%m%d')
        except ValueError:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                raise ValueError(f"无法解析日期: {date_str}")
    elif isinstance(date_str, datetime):
        date = date_str
    else:
        raise ValueError(f"无效的日期类型: {type(date_str)}")

    return date.strftime('%Y%m%d')

@date_range_checker
def some_func_1(start_date=None, end_date=None, increment=True):
    """
    获取指定日期范围内的数据。

    Args:
        start_date (str, optional): 开始日期，格式为 'YYYYMMDD' 或 'YYYY-MM-DD'。默认为当前日期。
        end_date (str, optional): 结束日期，格式为 'YYYYMMDD' 或 'YYYY-MM-DD'。如果为None，则使用当前非周末日期。
        increment (bool, optional): 是否增量获取数据。默认为True。

    Returns:
        list: 包含指定日期范围内数据的列表。
    """
    if start_date is None:
        start_date = datetime.now().strftime('%Y%m%d')
    if end_date is None:
        end_date = get_current_none_weekend_date_str()

    # 这里应该是获取网络数据的逻辑
    # 为了示例，我们返回一个空列表
    return []


if __name__ == '__main__':
    some_func_1('20250101', '2040101')