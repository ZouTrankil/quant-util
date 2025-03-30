#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/03/2025.
@author: Air.Zou
"""
import os
import json
import sqlite3
from turtle import st
import pandas as pd
from io import StringIO
from functools import wraps
from datetime import datetime, timedelta
from utils import date_utils
from utils.date_utils import get_current_none_weekend_date_str
from utils.log_util import logger

# 数据库文件路径
DB_PATH = "./cache"

def ensure_db_exists(table_name):
    """确保数据库存在"""
    # 确保目录存在
    db_path = os.path.join(DB_PATH, f"{table_name}.db")
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        logger.info(f"已创建缓存目录: {os.path.dirname(db_path)}")
    return db_path

def permenant_cache():
    """
    永久缓存装饰器
    使用单独的数据库表存储函数的返回值
    如果缓存需要更新则调用函数获取返回值，否则直接用数据库的缓存返回
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            table_name = func.__name__
            db_path = ensure_db_exists(table_name)

            # 检查是否需要更新
            need_update = False
            if os.path.exists(db_path):
                # 连接数据库
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # 检查表是否存在
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                if cursor.fetchone():
                    # 查询最新的更新时间
                    cursor.execute(f"SELECT update_time FROM {table_name} ORDER BY update_time DESC LIMIT 1")
                    result = cursor.fetchone()
                    if result:
                        # 返回结果
                        return result[0]
                    else:
                        need_update = True
                else:
                    need_update = True
            else:
                need_update = True

            # 如果需要更新或无法从缓存读取，调用原始函数
            if need_update:
                logger.info(f"调用原始函数获取数据: 函数={func.__name__}")
                result = func(*args, **kwargs)

                # 确保结果是DataFrame
                if isinstance(result, pd.DataFrame):
                    # 连接数据库
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()

                    # 确保表存在
                    cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        update_time TIMESTAMP,
                        data_csv TEXT,
                        PRIMARY KEY (update_time)
                    )
                    ''')

                    # 保存结果
                    data_csv = result.to_csv(index=False)
                    cursor.execute(f"INSERT OR REPLACE INTO {table_name} (update_time, data_csv) VALUES (?, ?)",
                                 (datetime.now(), data_csv))

                    conn.commit()
                    conn.close()
                    logger.info(f"缓存更新完成: 函数={func.__name__}, 行数={len(result)}")

                return result
        return wrapper
    return decorator

def every_day_update():
    """
    每天更新一次缓存装饰器
    使用单独的数据库表存储函数的返回值
    如果缓存需要更新则调用函数获取返回值，否则直接用数据库的缓存返回
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            table_name = func.__name__
            db_path = ensure_db_exists(table_name)
            valid_today = get_current_none_weekend_date_str()

            # 检查是否需要更新
            need_update = True
            if os.path.exists(db_path):
                # 连接数据库
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # 检查表是否存在
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                if cursor.fetchone():
                    # 查询最新的更新时间
                    cursor.execute(f"SELECT update_time FROM {table_name} ORDER BY update_time DESC LIMIT 1")
                    result = cursor.fetchone()
                    if result:
                        update_time = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S.%f")
                        # 检查是否是今天更新的
                        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                        if update_time >= today:
                            need_update = False
                            logger.info(f"缓存已是最新: 函数={func.__name__}, 日期={valid_today}")

                # 如果不需要更新，从缓存读取数据
                if not need_update:
                    cursor.execute(f"SELECT data_csv FROM {table_name} WHERE date_key = ?", (valid_today,))
                    result = cursor.fetchone()
                    if result:
                        try:
                            df = pd.read_csv(StringIO(result[0]))
                            logger.info(f"从缓存读取数据: 函数={func.__name__}, 日期={valid_today}, 行数={len(df)}")
                            conn.close()
                            return df
                        except Exception as e:
                            logger.error(f"缓存数据解析错误: 函数={func.__name__}, 日期={valid_today}, 错误={str(e)}")
                            need_update = True

                conn.close()

            # 如果需要更新或无法从缓存读取，调用原始函数
            if need_update:
                logger.info(f"调用原始函数获取数据: 函数={func.__name__}, 日期={valid_today}")
                result = func(*args, **kwargs)

                # 确保结果是DataFrame
                if isinstance(result, pd.DataFrame):
                    # 连接数据库
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()

                    # 确保表存在
                    cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        date_key TEXT,
                        update_time TIMESTAMP,
                        data_csv TEXT,
                        PRIMARY KEY (date_key)
                    )
                    ''')

                    # 保存结果
                    data_csv = result.to_csv(index=False)
                    cursor.execute(f"INSERT OR REPLACE INTO {table_name} (date_key, update_time, data_csv) VALUES (?, ?, ?)",
                                 (valid_today, datetime.now(), data_csv))

                    conn.commit()
                    conn.close()
                    logger.info(f"缓存更新完成: 函数={func.__name__}, 日期={valid_today}, 行数={len(result)}")

                return result

        return wrapper
    return decorator

def date_range_cache_with_symbol(symbol_key='symbol'):
    """
    日期范围缓存装饰器
    使用单独的数据库表存储函数的返回值，以日期和唯一标识(如股票代码)为键
    只获取缺失的日期数据，将其存入缓存，并与已有缓存数据合并返回

    缓存永久有效，只要数据库中存在就使用缓存，不存在才调用原始函数
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取函数的参数
            func_params = func.__code__.co_varnames[:func.__code__.co_argcount]
            all_args = dict(zip(func_params, args))
            all_args.update(kwargs)

            # 提取参数
            start_date = all_args.get('start_date')
            end_date = all_args.get('end_date')
            symbol = all_args.get('symbol', all_args.get('code', all_args.get('symbol_key', '')))

            # 确保日期格式正确
            if start_date:
                start_date = standardize_date(start_date)
            else:
                start_date = datetime.now().strftime('%Y%m%d')

            if end_date:
                end_date = standardize_date(end_date)
            else:
                end_date = get_current_none_weekend_date_str()

            # 获取日期范围
            date_range = date_utils.get_exchange_days(start_date=start_date, end_date=end_date)

            # 日志记录
            logger.info(f"日期范围缓存查询: 函数={func.__name__}, 标识={symbol}, 日期范围={start_date}至{end_date}, 共{len(date_range)}天")

            # 数据库连接
            table_name = func.__name__
            db_path = ensure_db_exists(table_name)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # 确保数据表存在
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            if not cursor.fetchone():
                cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    date_key TEXT,
                    symbol TEXT,
                    update_time TIMESTAMP,
                    data_csv TEXT,
                    PRIMARY KEY (date_key, symbol)
                )
                ''')
                conn.commit()
                logger.info(f"创建新表: {table_name}")

            # 检查哪些日期已有缓存
            cached_results = {}
            missing_dates = []
            cached_dates_count = 0

            for date_key in date_range:
                # 查询缓存
                cursor.execute(
                    f"SELECT data_csv FROM {table_name} WHERE date_key = ? AND symbol = ?",
                    (date_key, symbol)
                )
                cache_result = cursor.fetchone()

                # 检查缓存是否存在
                if cache_result:
                    try:
                        # 从CSV字符串恢复DataFrame
                        cached_results[date_key] = pd.read_csv(StringIO(cache_result[0]))
                        cached_dates_count += 1
                        logger.debug(f"缓存命中: 函数={func.__name__}, 标识={symbol}, 日期={date_key}")
                    except Exception as e:
                        missing_dates.append(date_key)
                        logger.error(f"缓存数据解析错误: 函数={func.__name__}, 标识={symbol}, 日期={date_key}, 错误={str(e)}")
                else:
                    # 缓存不存在
                    missing_dates.append(date_key)
                    logger.debug(f"缓存未命中: 函数={func.__name__}, 标识={symbol}, 日期={date_key}")

            # 如果所有日期都已缓存，直接返回
            if not missing_dates:
                conn.close()
                logger.info(f"全部从缓存读取: 函数={func.__name__}, 标识={symbol}, 命中数量={cached_dates_count}")
                return organize_date_results(cached_results, date_range)

            # 如果有缺失日期，调用原始函数获取缺失数据
            logger.info(f"调用接口获取缺失数据: 函数={func.__name__}, 标识={symbol}, 缺失日期={missing_dates[0]}至{missing_dates[-1]}, 共{len(missing_dates)}天")

            # 仅传递缺失日期范围和必要参数
            api_args = all_args.copy()
            api_args['start_date'] = missing_dates[0]
            api_args['end_date'] = missing_dates[-1]

            # 调用原始函数
            missing_results = func(**api_args)

            # 处理返回结果并存入缓存
            now = datetime.now()
            if isinstance(missing_results, dict):
                # 结果是字典，键为日期，值为DataFrame
                for date_key, value in missing_results.items():
                    if isinstance(value, pd.DataFrame) and date_key in missing_dates:
                        # 存入缓存
                        data_csv = value.to_csv(index=False)
                        cursor.execute(
                            f"INSERT OR REPLACE INTO {table_name} (date_key, symbol, update_time, data_csv) VALUES (?, ?, ?, ?)",
                            (date_key, symbol, now, data_csv)
                        )
                        logger.debug(f"缓存写入: 函数={func.__name__}, 标识={symbol}, 日期={date_key}, 数据行数={len(value)}")

                        # 更新结果集
                        cached_results[date_key] = value
            elif isinstance(missing_results, pd.DataFrame) and len(missing_dates) == 1:
                # 单日结果是DataFrame
                date_key = missing_dates[0]
                data_csv = missing_results.to_csv(index=False)
                cursor.execute(
                    f"INSERT OR REPLACE INTO {table_name} (date_key, symbol, update_time, data_csv) VALUES (?, ?, ?, ?)",
                    (date_key, symbol, now, data_csv)
                )
                logger.debug(f"缓存写入: 函数={func.__name__}, 标识={symbol}, 日期={date_key}, 数据行数={len(missing_results)}")
                cached_results[date_key] = missing_results

            conn.commit()
            conn.close()
            logger.info(f"缓存更新完成: 函数={func.__name__}, 标识={symbol}, 更新数量={len(missing_dates)}")

            # 返回合并后的结果
            return organize_date_results(cached_results, date_range)

        return wrapper
    return decorator

def organize_date_results(cached_results, date_range):
    """
    根据日期范围重新组织缓存结果
    如果只有一个日期，返回该日期的数据
    如果有多个日期，返回一个字典，键为日期，值为对应数据
    """
    if len(date_range) == 1:
        return cached_results.get(date_range[0])
    else:
        # 按照日期顺序返回结果
        return {date: cached_results.get(date) for date in date_range if date in cached_results}

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

# 使用每日更新装饰器示例
@every_day_update()
def get_daily_market_status():
    """获取每日市场状态数据，每天只需要更新一次"""
    # 模拟获取数据
    df = pd.DataFrame({
        'date': [get_current_none_weekend_date_str()],
        'status': ['正常'],
        'market_cap': [40000000000000],
        'volume': [50000000000]
    })
    return df

# 使用永久缓存装饰器示例
@permenant_cache()
def get_market_status():
    """获取市场状态数据，永久缓存"""
    # 模拟获取数据
    df = pd.DataFrame({
        'date': [get_current_none_weekend_date_str()],
        'status': ['正常'],
        'market_cap': [40000000000000],
        'volume': [50000000000]
    })
    return df

# 使用日期范围缓存装饰器示例
@date_range_cache_with_symbol()
def get_stock_daily_data(start_date, end_date, symbol):
    """获取股票日线数据，按日期和股票代码缓存"""
    # 生成日期范围
    date_range = date_utils.get_exchange_days(start_date=start_date, end_date=end_date)

    # 模拟获取股票数据
    result = {}
    for date in date_range:
        df = pd.DataFrame({
            'symbol': [symbol],
            'date': [date],
            'open': [100.0],
            'high': [105.0],
            'low': [98.0],
            'close': [102.0],
            'volume': [1000000]
        })
        result[date] = df

    return result

if __name__ == '__main__':
    # 测试每日更新装饰器
    market_status = get_daily_market_status()
    print("市场状态:\n", market_status)

    # 测试永久缓存装饰器
    market_status = get_market_status()
    print("市场状态:\n", market_status)

    # 测试日期范围缓存装饰器
    # 第一次调用，从接口获取数据
    stock_data = get_stock_daily_data('20240130', '20240205', '000001.SZ')
    print("股票数据(第一次调用):\n", stock_data)

    # 第二次调用，从缓存获取数据
    stock_data = get_stock_daily_data('20240130', '20240205', '000001.SZ')
    print("股票数据(第二次调用，应从缓存获取):\n", stock_data)

    # 调用部分缓存日期，部分新日期
    stock_data = get_stock_daily_data('20240130', '20240210', '000001.SZ')
    print("股票数据(日期范围扩展):\n", stock_data)

    # 调用不同股票代码
    stock_data = get_stock_daily_data('20240130', '20240205', '600000.SH')
    print("股票数据(不同股票代码):\n", stock_data)
