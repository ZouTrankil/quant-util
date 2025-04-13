"""
工具函数模块

此模块包含量化交易中常用的工具函数，如数值格式化、涨跌幅计算等。
"""

from typing import Optional, Union, Dict, Any, Tuple
import re


def format_number(value: float, precision: int = 2) -> str:
    """将数值格式化为指定精度的字符串

    Args:
        value (float): 待格式化的数值
        precision (int, optional): 小数点精度. 默认为2.

    Returns:
        str: 格式化后的字符串
    """
    return f"{value:.{precision}f}"


def get_number_desc(value: float) -> str:
    """使用亿、万作为单位显示大数值

    Args:
        value (float): 数值

    Returns:
        str: 格式化后的字符串，如"1.23亿"、"456.7万"
    """
    if value > 100000000.0:
        return f"{round(value / 100000000.0, 2)}亿"
    elif value > 10000.0:
        return f"{round(value / 10000.0, 0)}万"
    return f"{round(value, 0)}"


def calculate_change_percent(current: float, base: float) -> float:
    """计算变化百分比

    Args:
        current (float): 当前值
        base (float): 基准值

    Returns:
        float: 变化百分比，如涨幅5.2%返回5.2
    """
    if base == 0:
        return 0
    return round((current - base) * 100 / base, 2)


def get_rise_limit_by_stock_code(stock_code: str) -> float:
    """根据证券代码获取涨幅限制

    Args:
        stock_code (str): 证券代码，如'600000'

    Returns:
        float: 涨幅限制，如0.1表示10%，0.2表示20%
    """
    # 上证主板
    if stock_code.startswith('60'):
        return 0.1
    # 上证科创板
    if stock_code.startswith('68'):
        return 0.2
    # 深证主板
    if stock_code.startswith('00'):
        return 0.1
    # 深证创业板
    if stock_code.startswith('30'):
        return 0.2
    # 默认涨幅限制
    return 0.1


def normalize_stock_code(stock_code: str) -> str:
    """规范化证券代码

    将带交易所后缀的代码转换为纯数字代码

    Args:
        stock_code (str): 原始证券代码，如'600000.SH'

    Returns:
        str: 规范化后的证券代码，如'600000'
    """
    if '.' in stock_code:
        return stock_code.split('.')[0]
    return stock_code


def get_exchange_from_stock_code(stock_code: str) -> str:
    """从证券代码获取交易所代码

    Args:
        stock_code (str): 证券代码，如'600000'

    Returns:
        str: 交易所代码，'SH'或'SZ'
    """
    if '.' in stock_code:
        parts = stock_code.split('.')
        if len(parts) > 1:
            return parts[1]

    # 根据证券代码规则判断交易所
    code = normalize_stock_code(stock_code)
    if code.startswith(('60', '68')):
        return 'SH'
    elif code.startswith(('00', '30')):
        return 'SZ'
    return ''


def format_stock_code_with_exchange(stock_code: str) -> str:
    """格式化证券代码，加上交易所后缀

    Args:
        stock_code (str): 原始证券代码，如'600000'

    Returns:
        str: 带交易所后缀的证券代码，如'600000.SH'
    """
    if '.' in stock_code:
        return stock_code

    exchange = get_exchange_from_stock_code(stock_code)
    if exchange:
        return f"{normalize_stock_code(stock_code)}.{exchange}"
    return stock_code


def is_stock_rise_limit(price: float, last_close: float, stock_code: str) -> bool:
    """判断股票是否涨停

    Args:
        price (float): 当前价格
        last_close (float): 昨收价
        stock_code (str): 证券代码

    Returns:
        bool: 是否涨停
    """
    rise_limit = get_rise_limit_by_stock_code(stock_code)
    limit_price = round(last_close * (1 + rise_limit), 2)
    return round(price, 2) >= limit_price


def is_stock_fall_limit(price: float, last_close: float, stock_code: str) -> bool:
    """判断股票是否跌停

    Args:
        price (float): 当前价格
        last_close (float): 昨收价
        stock_code (str): 证券代码

    Returns:
        bool: 是否跌停
    """
    rise_limit = get_rise_limit_by_stock_code(stock_code)
    limit_price = round(last_close * (1 - rise_limit), 2)
    return round(price, 2) <= limit_price


def calculate_volume_ratio(current_volume: float, avg_volume: float) -> float:
    """计算量比

    Args:
        current_volume (float): 当前成交量
        avg_volume (float): 平均成交量

    Returns:
        float: 量比
    """
    if avg_volume == 0:
        return 0
    return round(current_volume / avg_volume, 2)
