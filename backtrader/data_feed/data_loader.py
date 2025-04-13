"""
数据加载模块

提供数据加载和预处理功能：
- 从文件加载数据
- 从数据库加载数据
- 从API加载数据
- 数据格式转换
"""

import pandas as pd
import backtrader as bt
from typing import Union, Optional
from datetime import datetime

class DataLoader:
    """数据加载器类"""

    @staticmethod
    def load_from_csv(file_path: str,
                     datetime_column: str = 'datetime',
                     datetime_format: str = '%Y-%m-%d',
                     **kwargs) -> bt.feeds.PandasData:
        """
        从CSV文件加载数据

        Args:
            file_path: 文件路径
            datetime_column: 日期时间列名
            datetime_format: 日期时间格式
            **kwargs: 其他参数

        Returns:
            bt.feeds.PandasData: 回测数据
        """
        df = pd.read_csv(file_path)
        df[datetime_column] = pd.to_datetime(df[datetime_column], format=datetime_format)
        df.set_index(datetime_column, inplace=True)
        return bt.feeds.PandasData(dataname=df, **kwargs)

    @staticmethod
    def load_from_dataframe(df: pd.DataFrame,
                          datetime_column: str = 'datetime',
                          **kwargs) -> bt.feeds.PandasData:
        """
        从DataFrame加载数据

        Args:
            df: 数据DataFrame
            datetime_column: 日期时间列名
            **kwargs: 其他参数

        Returns:
            bt.feeds.PandasData: 回测数据
        """
        if datetime_column in df.columns:
            df[datetime_column] = pd.to_datetime(df[datetime_column])
            df.set_index(datetime_column, inplace=True)
        return bt.feeds.PandasData(dataname=df, **kwargs)

    @staticmethod
    def resample_data(data: bt.feeds.PandasData,
                     timeframe: bt.TimeFrame,
                     compression: int) -> bt.feeds.PandasData:
        """
        重采样数据

        Args:
            data: 原始数据
            timeframe: 时间周期
            compression: 压缩比例

        Returns:
            bt.feeds.PandasData: 重采样后的数据
        """
        return bt.feeds.PandasData(dataname=data.resample(
            timeframe=timeframe,
            compression=compression
        ))
