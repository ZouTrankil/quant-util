"""
测试策略类

实现一个简单的均线交叉策略用于测试
"""

import backTest as bt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Any, Dict

class TestStrategy(bt.Strategy):
    """测试策略类"""

    params = (
        ('fast_period', 5),
        ('slow_period', 20),
    )

    def __init__(self):
        """初始化策略"""
        # 计算快速和慢速均线
        self.fast_ma = bt.indicators.SMA(period=self.params.fast_period)
        self.slow_ma = bt.indicators.SMA(period=self.params.slow_period)

        # 计算均线交叉信号
        self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)

    def next(self):
        """策略逻辑"""
        if not self.position:  # 没有持仓
            if self.crossover > 0:  # 金叉
                self.buy()
        else:  # 有持仓
            if self.crossover < 0:  # 死叉
                self.sell()

def create_test_data():
    """
    创建测试数据

    Returns:
        pd.DataFrame: 测试数据
    """
    # 生成随机价格数据
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', end='2020-12-31', freq='D')
    n = len(dates)

    # 生成随机游走价格
    returns = np.random.normal(0.001, 0.02, n)
    price = 100 * (1 + returns).cumprod()

    # 创建DataFrame
    df = pd.DataFrame({
        'datetime': dates,
        'open': price,
        'high': price * 1.01,
        'low': price * 0.99,
        'close': price,
        'volume': np.random.randint(1000, 10000, n)
    })

    return df
