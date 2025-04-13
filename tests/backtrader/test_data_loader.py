"""
数据加载器测试用例

测试数据加载器的各项功能：
- 从CSV加载数据
- 从DataFrame加载数据
- 数据重采样
"""

import unittest
import pandas as pd
import numpy as np
import os
from datetime import datetime
import backtrader as bt
from backtrader import TimeFrame

from quant_util.backtrader.data_feed.data_loader import DataLoader
from tests.backtrader.test_strategy import create_test_data

class TestDataLoader(unittest.TestCase):
    """数据加载器测试类"""

    def setUp(self):
        """测试初始化"""
        # 创建测试数据
        self.test_data = create_test_data()

        # 保存为CSV文件
        self.csv_file = 'test_data.csv'
        self.test_data.to_csv(self.csv_file, index=False)

    def tearDown(self):
        """测试清理"""
        # 删除测试文件
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def test_load_from_csv(self):
        """测试从CSV加载数据"""
        data = DataLoader.load_from_csv(
            self.csv_file,
            datetime_column='datetime',
            datetime_format='%Y-%m-%d'
        )

        # 检查数据格式
        self.assertIsInstance(data, bt.feeds.PandasData)
        self.assertEqual(len(data), len(self.test_data))

    def test_load_from_dataframe(self):
        """测试从DataFrame加载数据"""
        data = DataLoader.load_from_dataframe(
            self.test_data,
            datetime_column='datetime'
        )

        # 检查数据格式
        self.assertIsInstance(data, bt.feeds.PandasData)
        self.assertEqual(len(data), len(self.test_data))

    def test_resample_data(self):
        """测试数据重采样"""
        # 首先加载数据
        data = DataLoader.load_from_dataframe(
            self.test_data,
            datetime_column='datetime'
        )

        # 重采样为周线
        weekly_data = DataLoader.resample_data(
            data,
            timeframe=TimeFrame.Weeks,
            compression=1
        )

        # 检查重采样结果
        self.assertIsInstance(weekly_data, bt.feeds.PandasData)
        self.assertLess(len(weekly_data), len(data))  # 周线数据应该更少

    def test_data_validation(self):
        """测试数据验证"""
        # 创建无效数据（缺少必要列）
        invalid_data = self.test_data.drop(columns=['close'])

        # 测试加载无效数据
        with self.assertRaises(Exception):
            DataLoader.load_from_dataframe(
                invalid_data,
                datetime_column='datetime'
            )

if __name__ == '__main__':
    unittest.main()
