#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/03/2025.
@author: Air.Zou
"""
import os
import json
import sqlite3
from functools import wraps
from datetime import datetime, timedelta
from utils.date_utils import get_current_none_weekend_date_str


# 数据库文件路径
DB_PATH = "./cache/local_cache.db"

def ensure_db_exists():
    """确保数据库存在并创建必要的表"""
    # 确保目录存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # 创建连接和表
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建缓存表 - 每个时间点单独存储
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cache (
        func_name TEXT,
        date_key TEXT,
        update_time TIMESTAMP,
        data TEXT,
        PRIMARY KEY (func_name, date_key)
    )
    ''')
    
    conn.commit()
    conn.close()

def local_data_cache(update_frequency=1):
    """
    装饰器工厂函数，用于创建日期范围检查器装饰器。
    使用SQLite数据库存储缓存数据，每个时间点独立存储。

    Args:
        update_frequency (int, optional): 更新频率（天）。默认为1天。
    """
    # 确保数据库和表存在
    ensure_db_exists()

    def decorator(func):
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
            
            # 生成日期范围内的所有日期
            date_range = generate_date_range(start_date, end_date)
            
            # 连接数据库
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            now = datetime.now()
            cached_results = {}
            missing_dates = []
            
            # 检查每个日期的缓存
            for date_key in date_range:
                # 查询缓存
                cursor.execute(
                    "SELECT data, update_time FROM cache WHERE func_name = ? AND date_key = ?",
                    (func.__name__, date_key)
                )
                cache_result = cursor.fetchone()
                
                if cache_result:
                    data, update_time_str = cache_result
                    update_time = datetime.strptime(update_time_str, "%Y-%m-%d %H:%M:%S.%f")
                    days_since_update = (now - update_time).days
                    
                    # 如果缓存存在且未过期，加入结果集
                    if days_since_update < update_frequency:
                        cached_results[date_key] = json.loads(data)
                        continue
                
                # 如果没有有效缓存，添加到缺失日期列表
                missing_dates.append(date_key)
            
            # 如果所有日期都已缓存，直接返回结果
            if not missing_dates:
                conn.close()
                # 根据原始函数返回类型组织数据
                return organize_results(cached_results, date_range)
            
            # 如果有缺失日期，需要调用原始函数获取数据
            # 使用原始的start_date和end_date调用函数
            result = func(**all_args)
            
            # 如果结果是字典，假设键是日期
            if isinstance(result, dict):
                for date_key, value in result.items():
                    # 保存到数据库
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO cache (func_name, date_key, update_time, data)
                        VALUES (?, ?, ?, ?)
                        """,
                        (func.__name__, date_key, now, json.dumps(value))
                    )
                    # 更新缓存结果
                    cached_results[date_key] = value
            # 如果结果是列表，假设每个元素对应一个日期
            elif isinstance(result, list) and len(result) == len(missing_dates):
                for i, date_key in enumerate(missing_dates):
                    value = result[i]
                    # 保存到数据库
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO cache (func_name, date_key, update_time, data)
                        VALUES (?, ?, ?, ?)
                        """,
                        (func.__name__, date_key, now, json.dumps(value))
                    )
                    # 更新缓存结果
                    cached_results[date_key] = value
            # 如果是其他类型或无法映射到日期，将整个结果缓存在每个日期下
            else:
                for date_key in missing_dates:
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO cache (func_name, date_key, update_time, data)
                        VALUES (?, ?, ?, ?)
                        """,
                        (func.__name__, date_key, now, json.dumps(result))
                    )
                    # 对于无法映射的情况，每个日期都存储完整结果
                    cached_results[date_key] = result
            
            conn.commit()
            conn.close()
            
            # 返回组织好的结果
            return organize_results(cached_results, date_range)

        return wrapper

    return decorator


def generate_date_range(start_date, end_date):
    """生成从start_date到end_date的所有日期字符串列表"""
    start = datetime.strptime(start_date, '%Y%m%d')
    end = datetime.strptime(end_date, '%Y%m%d')
    
    date_range = []
    current = start
    
    while current <= end:
        date_range.append(current.strftime('%Y%m%d'))
        current += timedelta(days=1)
    
    return date_range


def organize_results(cached_results, date_range):
    """
    根据日期范围重新组织缓存结果
    如果只有一个日期，返回该日期的数据
    如果有多个日期，返回一个字典，键为日期，值为对应数据
    """
    if len(date_range) == 1:
        return cached_results[date_range[0]]
    else:
        # 按照日期顺序返回结果
        return {date: cached_results.get(date) for date in date_range}


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


@local_data_cache(update_frequency=1)
def some_func_1(start_date=None, end_date=None):
    """
    获取指定日期范围内的数据。

    Args:
        start_date (str, optional): 开始日期，格式为 'YYYYMMDD' 或 'YYYY-MM-DD'。默认为当前日期。
        end_date (str, optional): 结束日期，格式为 'YYYYMMDD' 或 'YYYY-MM-DD'。如果为None，则使用当前非周末日期。
        increment (bool, optional): 是否增量获取数据。默认为True。

    Returns:
        dict: 包含指定日期范围内数据的字典，键为日期，值为该日期的数据。
    """
    if start_date is None:
        start_date = datetime.now().strftime('%Y%m%d')
    if end_date is None:
        end_date = get_current_none_weekend_date_str()

    # 生成日期范围
    date_range = generate_date_range(standardize_date(start_date), standardize_date(end_date))
    
    # 模拟获取网络数据
    result = {}
    for date in date_range:
        result[date] = {"data": f"数据 for {date}"}
    
    return result

permanent_cache = local_data_cache(update_frequency=100000)

@permanent_cache
def some_func_2(start_date=None, end_date=None):
    print(start_date, end_date)
    
    # 返回单个日期的数据
    if start_date == end_date or end_date is None:
        date = standardize_date(start_date) if start_date else get_current_none_weekend_date_str()
        return {"单日数据": f"数据 for {date}"}
    
    # 返回日期范围的数据
    date_range = generate_date_range(standardize_date(start_date), standardize_date(end_date))
    result = {}
    for date in date_range:
        result[date] = {"数据项": f"数据 for {date}"}
    
    return result
    
if __name__ == '__main__':
    # 测试单日查询
    print(some_func_1('20250101', '20250101'))
    
    # 测试日期范围查询
    result = some_func_1('20250101', '20250105')
    for date, data in result.items():
        print(f"{date}: {data}")
    
    # 测试永久缓存
    some_func_2('20250110', '20250115')
