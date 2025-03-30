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

if __name__ == '__main__':
    # 测试每日更新装饰器
    market_status = get_daily_market_status()
    print("市场状态:\n", market_status)
