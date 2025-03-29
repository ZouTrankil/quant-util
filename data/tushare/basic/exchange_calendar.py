#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/03/2025.
@author: Air.Zou
"""
from typing import List, Optional, Set, Dict
import os
import pickle
from bisect import bisect_left, bisect_right

from utils.date_utils import get_current_date_str
from utils.global_config import DataSource

CACHE_DIR = './cache/trade_calendar'

# 缓存文件路径
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)
TRADE_DAYS_CACHE = os.path.join(CACHE_DIR, 'trade_days_v2.pkl')

def _encode_date(date_str: str) -> int:
    """将日期字符串编码为整数
    例如: '20250101' -> 20250101
    """
    return int(date_str)

def _decode_date(date_int: int) -> str:
    """将整数解码为日期字符串
    例如: 20250101 -> '20250101'
    """
    return f"{date_int:08d}"

class TradeCalendar:
    def __init__(self):
        self._trade_days: Set[int] = set()
        self._sorted_days: List[int] = []
        self._load_cache()

    def _load_cache(self):
        """加载或初始化缓存"""
        if os.path.exists(TRADE_DAYS_CACHE):
            try:
                with open(TRADE_DAYS_CACHE, 'rb') as f:
                    cache_data = pickle.load(f)
                    self._trade_days = cache_data['days']
                    self._sorted_days = sorted(list(self._trade_days))
                return
            except Exception:
                pass
        self._update_cache()

    def _update_cache(self, force: bool = False):
        """更新缓存数据"""
        current_date = get_current_date_str()
        result = DataSource.tushare_pro.trade_cal(
            exchange='',
            start_date='19900101',
            end_date=current_date
        )
        trade_days = set(
            _encode_date(date)
            for date in result[result['is_open'] == 1]['cal_date'].tolist()
        )

        self._trade_days = trade_days
        self._sorted_days = sorted(list(trade_days))

        # 保存缓存
        with open(TRADE_DAYS_CACHE, 'wb') as f:
            pickle.dump({
                'days': self._trade_days,
                'last_update': current_date
            }, f)

    def get_trade_days(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[str]:
        """获取指定范围内的交易日列表"""
        if end_date is None:
            end_date = get_current_date_str()

        start_int = _encode_date(start_date) if start_date else 0
        end_int = _encode_date(end_date)

        # 使用二分查找快速定位范围
        start_idx = bisect_left(self._sorted_days, start_int)
        end_idx = bisect_right(self._sorted_days, end_int)

        return [_decode_date(day) for day in self._sorted_days[start_idx:end_idx]]

    def is_trade_day(self, date_str: str) -> bool:
        """判断是否为交易日"""
        return _encode_date(date_str) in self._trade_days

    def get_prev_trade_day(self, date_str: str) -> str:
        """获取前一个交易日"""
        date_int = _encode_date(date_str)
        idx = bisect_left(self._sorted_days, date_int)

        if idx > 0:
            if self._sorted_days[idx] == date_int:
                return _decode_date(self._sorted_days[idx - 1])
            return _decode_date(self._sorted_days[idx - 1])
        return ""

    def get_next_trade_day(self, date_str: str) -> str:
        """获取下一个交易日"""
        date_int = _encode_date(date_str)
        idx = bisect_right(self._sorted_days, date_int)

        if idx < len(self._sorted_days):
            return _decode_date(self._sorted_days[idx])
        return ""

# 全局单例
_calendar = TradeCalendar()

def get_trade_days_info(start_date: Optional[str] = None, end_date: Optional[str] = None):
    """保留原接口，用于直接访问tushare数据"""
    if end_date is None:
        end_date = get_current_date_str()
    return DataSource.tushare_pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)

def get_trade_days_str(start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[str]:
    """获取交易日列表"""
    return _calendar.get_trade_days(start_date, end_date)

def is_trade_day(date_str: str) -> bool:
    """判断是否为交易日"""
    return _calendar.is_trade_day(date_str)

def get_prev_trade_day(date_str: str) -> str:
    """获取前一个交易日"""
    return _calendar.get_prev_trade_day(date_str)

def get_next_trade_day(date_str: str) -> str:
    """获取下一个交易日"""
    return _calendar.get_next_trade_day(date_str)

if __name__ == '__main__':
    print(get_trade_days_str(start_date='20250101', end_date='20250401'))
    print(is_trade_day('20250101'))
    print(get_prev_trade_day('20250101'))
    print(get_next_trade_day('20250101'))

# result
#       exchange  cal_date  is_open pretrade_date
# 0          SSE  20251231        1      20251230
# 1          SSE  20251230        1      20251229
# 2          SSE  20251229        1      20251226
#
