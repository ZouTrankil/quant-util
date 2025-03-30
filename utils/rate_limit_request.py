#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/03/2025.
@author: Air.Zou
"""
import time
import threading
from functools import wraps
from collections import deque
from datetime import datetime
from utils.log_util import logger

class RateLimiter:
    """
    速率限制器，用于控制接口调用频率
    """
    def __init__(self, max_calls, time_window=60):
        """
        初始化速率限制器

        Args:
            max_calls (int): 在时间窗口内允许的最大调用次数
            time_window (int): 时间窗口大小，单位为秒，默认为60秒（1分钟）
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque(maxlen=max_calls)
        self.lock = threading.Lock()

    def __call__(self, func):
        """
        装饰器主体函数

        Args:
            func: 要装饰的函数

        Returns:
            wrapper: 包装后的函数
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self.lock:
                # 当前时间
                current_time = time.time()

                # 清理过期的调用记录
                while self.calls and current_time - self.calls[0] > self.time_window:
                    self.calls.popleft()

                # 如果调用次数已达到限制
                if len(self.calls) >= self.max_calls:
                    # 计算需要等待的时间
                    oldest_call = self.calls[0]
                    wait_time = oldest_call + self.time_window - current_time
                    if wait_time > 0:
                        logger.info(f"达到接口调用频率限制，等待 {wait_time:.2f} 秒")
                        time.sleep(wait_time)
                        # 更新当前时间
                        current_time = time.time()

                # 记录本次调用
                self.calls.append(current_time)

            # 调用原始函数
            return func(*args, **kwargs)

        return wrapper


def rate_limit(max_calls_per_minute):
    """
    限制接口调用频率的装饰器

    Args:
        max_calls_per_minute (int): 每分钟最大调用次数

    Returns:
        decorator: 装饰器函数
    """
    return RateLimiter(max_calls=max_calls_per_minute)


# 示例：使用装饰器限制接口调用频率
@rate_limit(max_calls_per_minute=5)
def api_request(endpoint, data=None):
    """
    模拟API请求

    Args:
        endpoint (str): API端点
        data (dict, optional): 请求数据

    Returns:
        dict: API响应
    """
    logger.info(f"调用API: {endpoint}")
    # 模拟API调用延迟
    time.sleep(0.5)
    return {"success": True, "endpoint": endpoint, "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    # 测试代码
    for i in range(15):
        result = api_request(f"/api/test/{i}")
        print(f"请求 {i}: {result['timestamp']}")

