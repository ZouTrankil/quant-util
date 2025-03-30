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
from datetime import datetime
from utils.global_config import DataSource
from utils.log_util import logger

# 设置日志级别为TRACE
logger.disable('INFO')

CACHE_DIR = './cache/trade_calendar'


def get_current_date_str():
    return datetime.now().strftime('%Y%m%d')

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
        current_date = get_current_date_str()

        # 检查是否需要更新缓存
        need_update = True

        if os.path.exists(TRADE_DAYS_CACHE):
            try:
                with open(TRADE_DAYS_CACHE, 'rb') as f:
                    cache_data = pickle.load(f)

                    # 检查缓存的最后更新日期
                    last_update_date = cache_data.get('last_update', '19900101')

                    # 如果最后更新日期是今天，则使用缓存
                    if last_update_date == current_date:
                        self._trade_days = cache_data['days']
                        self._sorted_days = sorted(list(self._trade_days))
                        logger.trace(f"使用今日交易日历缓存: {current_date}")
                        need_update = False
                    else:
                        logger.trace(f"交易日历缓存已过期: 缓存日期={last_update_date}, 当前日期={current_date}")

            except Exception as e:
                logger.error(f"读取交易日历缓存发生错误: {str(e)}")

        # 如果需要更新（缓存不存在、已过期或读取错误），则更新缓存
        if need_update:
            self._update_cache()

    def _update_cache(self, force: bool = False):
        """更新缓存数据"""
        current_date = get_current_date_str()
        logger.trace(f"更新交易日历缓存: 日期={current_date}, 强制更新={force}")

        if not force and len(self._sorted_days) > 0:  # 确保列表不为空
            try:
                # 查找缓存中最近的交易日期
                last_trade_day = self._sorted_days[-1]
                if last_trade_day == _encode_date(current_date):
                    logger.trace(f"缓存中最近的交易日期与当前日期相同: {current_date}")
                    return

                # 检查文件修改时间
                if os.path.exists(TRADE_DAYS_CACHE):
                    last_update_timestamp = os.path.getmtime(TRADE_DAYS_CACHE)
                    last_update_date = datetime.fromtimestamp(last_update_timestamp).strftime('%Y%m%d')
                    if last_update_date == current_date:
                        logger.trace(f"缓存文件今日已更新: {current_date}")
                        return
            except Exception as e:
                logger.error(f"检查缓存时发生错误: {str(e)}")
                # 出错时继续更新缓存

        try:
            # 确保缓存目录存在
            if not os.path.exists(CACHE_DIR):
                os.makedirs(CACHE_DIR)

            result = DataSource.tushare_pro.trade_cal(
                exchange='',
                start_date='19900101',
                end_date=current_date
            )

            if result is not None and not result.empty:
                trade_days = set(
                    _encode_date(date)
                    for date in result[result['is_open'] == 1]['cal_date'].tolist()
                )

                self._trade_days = trade_days
                self._sorted_days = sorted(list(trade_days))

                # 保存缓存，包含最后更新日期
                try:
                    with open(TRADE_DAYS_CACHE, 'wb') as f:
                        pickle.dump({
                            'days': self._trade_days,
                            'last_update': current_date
                        }, f)
                    logger.trace(f"交易日历缓存更新完成: 共{len(self._trade_days)}个交易日")
                except Exception as e:
                    logger.error(f"保存交易日历缓存时发生错误: {str(e)}")
            else:
                logger.warning("从数据源获取交易日历数据失败或返回为空")
        except Exception as e:
            logger.error(f"更新交易日历缓存时发生错误: {str(e)}")

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
        if not self._sorted_days:
            # 如果交易日列表为空，尝试更新缓存
            self._update_cache(force=True)
            if not self._sorted_days:
                logger.error("交易日历为空，无法获取前一个交易日")
                return ""

        date_int = _encode_date(date_str)

        # 检查日期是否超过最大交易日
        if date_int > self._sorted_days[-1]:
            # 如果日期大于最后一个交易日，直接返回最后一个交易日
            logger.trace(f"日期 {date_str} 大于最大交易日 {_decode_date(self._sorted_days[-1])}，返回最大交易日")
            return _decode_date(self._sorted_days[-1])

        # 正常二分查找
        idx = bisect_left(self._sorted_days, date_int)

        # 防止索引越界，日志记录调试信息
        if idx >= len(self._sorted_days):
            logger.trace(f"索引 {idx} 超出交易日列表长度 {len(self._sorted_days)}，返回最后一个交易日")
            return _decode_date(self._sorted_days[-1]) if self._sorted_days else ""

        # 如果找到了精确匹配
        if self._sorted_days[idx] == date_int:
            # 如果是第一个交易日，无法获取前一个
            if idx == 0:
                return ""
            return _decode_date(self._sorted_days[idx - 1])

        # 没有找到精确匹配，返回小于当前日期的最大交易日
        if idx > 0:
            return _decode_date(self._sorted_days[idx - 1])

        # 如果idx为0，说明没有更早的交易日
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

def force_update_trade_calendar():
    """强制更新交易日历"""
    _calendar._update_cache(force=True)
    return True

def get_recent_trade_day():
    """
    获取当前最近的交易日
    如果当前日期是交易日则返回当前日期，否则返回前一个交易日

    Returns:
        str: 格式为 'YYYYMMDD' 的最近交易日
    """
    today = get_current_date_str()
    if _calendar.is_trade_day(today):
        return today
    else:
        return _calendar.get_prev_trade_day(today)

def get_prev_trade_days(date_str, days_count=1):
    """
    获取指定日期前几个交易日
    如果指定日期不是交易日，会自动往前找最近的交易日

    Args:
        date_str (str): 日期字符串，格式为 'YYYYMMDD'
        days_count (int): 需要获取的前几个交易日数量
    """
    d = get_prev_trade_day(date_str)
    # 从 sorted_days 中找到 d 的 前第 days_count 个交易日
    idx = bisect_left(_calendar._sorted_days, _encode_date(d))
    # 返回第 idx - days_count 个交易日
    return _decode_date(_calendar._sorted_days[idx-days_count])

if __name__ == '__main__':
    print(get_trade_days_str(start_date='20250101', end_date='20250401'))
    print(is_trade_day('20250328'))
    print(get_prev_trade_day('20250101'))
    print(get_next_trade_day('20250101'))
    print(get_recent_trade_day())
    print(get_prev_trade_day('20250331'))
    print(get_prev_trade_days('20250331', 3))

# result
#       exchange  cal_date  is_open pretrade_date
# 0          SSE  20251231        1      20251230
# 1          SSE  20251230        1      20251229
# 2          SSE  20251229        1      20251226
#
