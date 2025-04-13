"""
回测引擎测试用例

测试回测引擎的各项功能：
- 数据加载
- 策略运行
- 结果分析
"""

import unittest
import backtrader as bt

from backtrader import BacktestEngine
from backtrader import DataLoader
from tests.backtrader.test_strategy import TestStrategy, create_test_data

class TestBacktestEngine(unittest.TestCase):
    """回测引擎测试类"""

    def setUp(self):
        """测试初始化"""
        self.engine = BacktestEngine(
            initial_cash=100000.0,
            commission=0.001,
            stake=1,
            slippage=0.0
        )

        # 创建测试数据
        self.test_data = create_test_data()
        self.data = DataLoader.load_from_dataframe(self.test_data)

    def test_add_data(self):
        """测试添加数据"""
        self.engine.add_data(self.data)
        self.assertEqual(len(self.engine.cerebro.datas), 1)

    def test_add_strategy(self):
        """测试添加策略"""
        self.engine.add_data(self.data)
        self.engine.add_strategy(TestStrategy)
        self.assertEqual(len(self.engine.cerebro.strats), 1)

    def test_run_backtest(self):
        """测试运行回测"""
        # 添加数据和策略
        self.engine.add_data(self.data)
        self.engine.add_strategy(TestStrategy)

        # 运行回测
        results = self.engine.run()

        # 检查结果
        self.assertIn('final_value', results)
        self.assertIn('return', results)
        self.assertIn('trades', results)
        self.assertIn('drawdown', results)
        self.assertIn('sharpe', results)
        self.assertIn('trade_analysis', results)

        # 检查资金曲线
        self.assertGreater(results['final_value'], 0)

    def test_plot(self):
        """测试绘图功能"""
        # 添加数据和策略
        self.engine.add_data(self.data)
        self.engine.add_strategy(TestStrategy)

        # 运行回测
        self.engine.run()

        # 测试绘图（这里只是测试是否抛出异常）
        try:
            self.engine.plot()
        except Exception as e:
            self.fail(f"绘图失败: {str(e)}")

    def test_analyzer(self):
        """测试分析器"""
        # 添加数据和策略
        self.engine.add_data(self.data)
        self.engine.add_strategy(TestStrategy)

        # 添加分析器
        self.engine.add_analyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        self.engine.add_analyzer(bt.analyzers.DrawDown, _name='drawdown')
        self.engine.add_analyzer(bt.analyzers.TradeAnalyzer, _name='trade')

        # 运行回测
        results = self.engine.run()

        # 检查分析结果
        self.assertIn('sharpe', results)
        self.assertIn('drawdown', results)
        self.assertIn('trade_analysis', results)

if __name__ == '__main__':
    unittest.main()
