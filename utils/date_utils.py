#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/03/2025.
@author: Air.Zou
"""

import datetime
from typing import List, Tuple
import sys
import os

# 确保能正确导入模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from data.tushare.basic import exchange_calendar

def judge_weekend(current_date):
    weekday = current_date.weekday()
    return weekday == 5 or weekday == 6

# 排除星期6和星期7
def get_current_exchange_day_str():
    today = get_current_date_str()
    if exchange_calendar.is_trade_day(today):
        return today
    else:
        return exchange_calendar.get_prev_trade_day(today)

def get_current_date_str():
    current_date = datetime.date.today()
    formatted_date = current_date.strftime("%Y%m%d")
    return formatted_date

def get_current_none_weekend_date_str():
    """
    获取当前日期，如果当前日期是周末，则返回最近的交易日

    Returns:
        str: 格式为 'YYYYMMDD' 的非周末日期字符串
    """
    current_date = datetime.date.today()
    # 如果是周末，则返回周五
    if judge_weekend(current_date):
        # 找到最近的交易日
        today_str = current_date.strftime("%Y%m%d")
        return exchange_calendar.get_prev_trade_day(today_str)
    return current_date.strftime("%Y%m%d")

def get_recent_trade_day():
    """
    获取当前最近的交易日
    如果当前日期是交易日则返回当前日期，否则返回前一个交易日

    Returns:
        str: 格式为 'YYYYMMDD' 的最近交易日
    """
    today = get_current_date_str()
    if exchange_calendar.is_trade_day(today):
        return today
    else:
        return exchange_calendar.get_prev_trade_day(today)

def get_trade_days_around(date_str, prev_days=1, next_days=1):
    """
    获取指定日期前后的交易日
    如果指定日期不是交易日，会自动往前找最近的交易日

    Args:
        date_str (str): 日期字符串，格式为 'YYYYMMDD'
        prev_days (int): 向前获取的交易日数量
        next_days (int): 向后获取的交易日数量

    Returns:
        dict: 包含以下键:
            - 'date': 修正后的日期
            - 'is_corrected': 是否进行了日期修正
            - 'prev_days': 前几个交易日列表
            - 'next_days': 后几个交易日列表
    """
    # 确保日期格式正确
    if isinstance(date_str, str):
        try:
            datetime.datetime.strptime(date_str, '%Y%m%d')
        except ValueError:
            try:
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                date_str = date.strftime('%Y%m%d')
            except ValueError:
                raise ValueError(f"无法解析日期: {date_str}")

    # 检查日期是否为交易日，如果不是则修正为前一个交易日
    is_corrected = False
    original_date = date_str
    if not exchange_calendar.is_trade_day(date_str):
        date_str = exchange_calendar.get_prev_trade_day(date_str)
        is_corrected = True

    if not date_str:
        raise ValueError(f"无法找到日期 {original_date} 对应的交易日")

    # 获取所有交易日
    all_trade_days = exchange_calendar.get_trade_days_str('19900101', get_current_date_str())

    # 找到日期在列表中的位置
    try:
        date_index = all_trade_days.index(date_str)
    except ValueError:
        raise ValueError(f"交易日 {date_str} 不在交易日列表中")

    # 获取前几个交易日
    start_index = max(0, date_index - prev_days)
    prev_trade_days = all_trade_days[start_index:date_index]

    # 获取后几个交易日
    end_index = min(len(all_trade_days), date_index + next_days + 1)
    next_trade_days = all_trade_days[date_index+1:end_index]

    return {
        'date': date_str,
        'is_corrected': is_corrected,
        'prev_days': prev_trade_days,
        'next_days': next_trade_days
    }

def get_days_ago(days):
    # 获取当前日期
    current_date = datetime.date.today()
    # 计算 days 天前的日期
    days_ago_date = current_date - datetime.timedelta(days=days)
    # 将日期转换为字符串
    formatted_date = days_ago_date.strftime("%Y%m%d")
    return formatted_date

def get_exchange_days(start_date, end_date) -> List[str]:
    return exchange_calendar.get_trade_days_str(start_date, end_date)

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

def get_prev_trade_days(date_str, days_count=1):
    """
    获取指定日期前几个交易日
    如果指定日期不是交易日，会自动往前找最近的交易日

    Args:
        date_str (str): 日期字符串，格式为 'YYYYMMDD'
        days_count (int): 需要获取的前几个交易日数量

    Returns:
        dict: 包含以下键:
            - 'date': 修正后的交易日期
            - 'is_corrected': 是否进行了日期修正
            - 'prev_days': 前几个交易日列表
    """
    # 确保日期格式正确
    if isinstance(date_str, str):
        try:
            datetime.datetime.strptime(date_str, '%Y%m%d')
        except ValueError:
            try:
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                date_str = date.strftime('%Y%m%d')
            except ValueError:
                raise ValueError(f"无法解析日期: {date_str}")

    # 检查日期是否为交易日，如果不是则修正为前一个交易日
    is_corrected = False
    original_date = date_str
    if not exchange_calendar.is_trade_day(date_str):
        date_str = exchange_calendar.get_prev_trade_day(date_str)
        is_corrected = True

    if not date_str:
        raise ValueError(f"无法找到日期 {original_date} 对应的交易日")

    # 获取所有交易日
    all_trade_days = exchange_calendar.get_trade_days_str('19900101', get_current_date_str())

    # 找到日期在列表中的位置
    try:
        date_index = all_trade_days.index(date_str)
    except ValueError:
        raise ValueError(f"交易日 {date_str} 不在交易日列表中")

    # 获取前几个交易日
    start_index = max(0, date_index - days_count)
    prev_trade_days = all_trade_days[start_index:date_index]

    return {
        'date': date_str,
        'is_corrected': is_corrected,
        'prev_days': prev_trade_days
    }


from datetime import datetime, timedelta
from typing import Union, Optional

def parse_datetime(dt_str: str, fmt: str = '%Y-%m-%d') -> datetime:
    """
    解析日期时间字符串

    Args:
        dt_str: 日期时间字符串
        fmt: 日期时间格式

    Returns:
        datetime: 日期时间对象
    """
    return datetime.strptime(dt_str, fmt)

def format_datetime(dt: datetime, fmt: str = '%Y-%m-%d') -> str:
    """
    格式化日期时间对象

    Args:
        dt: 日期时间对象
        fmt: 日期时间格式

    Returns:
        str: 格式化后的字符串
    """
    return dt.strftime(fmt)

def add_days(dt: datetime, days: int) -> datetime:
    """
    添加天数

    Args:
        dt: 日期时间对象
        days: 天数

    Returns:
        datetime: 新的日期时间对象
    """
    return dt + timedelta(days=days)

def date_range(start: Union[str, datetime],
               end: Union[str, datetime],
               fmt: str = '%Y-%m-%d') -> list[datetime]:
    """
    生成日期范围

    Args:
        start: 开始日期
        end: 结束日期
        fmt: 日期格式（如果输入是字符串）

    Returns:
        list[datetime]: 日期列表
    """
    if isinstance(start, str):
        start = parse_datetime(start, fmt)
    if isinstance(end, str):
        end = parse_datetime(end, fmt)

    days = (end - start).days + 1
    return [start + timedelta(days=x) for x in range(days)]


if __name__ == '__main__':
    print("当前日期:", get_current_date_str())
    print("2天前的日期:", get_days_ago(2))

    # 先强制更新交易日历
    exchange_calendar.force_update_trade_calendar()

    print("当前交易日:", get_current_exchange_day_str())
    print("当前非周末日期:", get_current_none_weekend_date_str())
    print("当前最近交易日:", get_recent_trade_day())

    try:
        # 测试获取指定日期前后的交易日
        print("\n测试获取指定日期前后的交易日:")
        result = get_trade_days_around('20250328', prev_days=3, next_days=3)
        print(f"日期: {result['date']}, 已修正: {result['is_corrected']}")
        print(f"前3个交易日: {result['prev_days']}")
        print(f"后3个交易日: {result['next_days']}")

        # 测试非交易日的情况
        print("\n周末日期测试 - 原始日期: 20250330")
        weekend_result = get_trade_days_around('20250330', prev_days=2, next_days=2)  # 周日
        print(f"修正后日期: {weekend_result['date']}, 已修正: {weekend_result['is_corrected']}")
        print(f"前2个交易日: {weekend_result['prev_days']}")
        print(f"后2个交易日: {weekend_result['next_days']}")

        # 测试获取前几个交易日
        print("\n测试获取前几个交易日:")
        prev_days_result = get_prev_trade_days('20250328', days_count=5)
        print(f"日期: {prev_days_result['date']}, 已修正: {prev_days_result['is_corrected']}")
        print(f"前5个交易日: {prev_days_result['prev_days']}")

        # 测试非交易日获取前几个交易日
        print("\n非交易日测试 - 原始日期: 20250330")
        weekend_prev_result = get_prev_trade_days('20250330', days_count=3)  # 周日
        print(f"修正后日期: {weekend_prev_result['date']}, 已修正: {weekend_prev_result['is_corrected']}")
        print(f"前3个交易日: {weekend_prev_result['prev_days']}")

    except Exception as e:
        print(f"测试时出现错误: {str(e)}")
