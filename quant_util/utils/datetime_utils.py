"""
日期时间工具模块

提供日期时间相关的工具函数
"""

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
