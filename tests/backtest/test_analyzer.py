"""
性能分析器测试用例

测试性能分析器的各项功能：
- 收益率分析
- 风险分析
- 交易分析
- 回撤分析
"""

import unittest

from backTest import PerformanceAnalyzer
from backTest import BacktestEngine
from backTest import DataLoader
from tests.backtrader.test_strategy import TestStrategy, create_test_data

class TestPerformanceAnalyzer(unittest.TestCase):
    """性能分析器测试类"""

    def setUp(self):
        """测试初始化"""
        # 创建回测引擎
        self.engine = BacktestEngine(
            initial_cash=100000.0,
            commission=0.001,
            stake=1,
            slippage=0.0
        )

        # 创建测试数据
        self.test_data = create_test_data()
        self.data = DataLoader.load_from_dataframe(self.test_data)

        # 添加数据和策略
        self.engine.add_data(self.data)
        self.engine.add_strategy(TestStrategy)

        # 创建性能分析器
        self.analyzer = PerformanceAnalyzer()
        self.analyzer.add_to_cerebro(self.engine.cerebro)

    def test_analyze_returns(self):
        """测试收益率分析"""
        # 运行回测
        self.engine.run()

        # 获取分析结果
        results = self.analyzer.analyze(self.engine.cerebro.runstrats[0][0])

        # 检查收益率结果
        self.assertIn('returns', results)
        self.assertIn('total_return', results['returns'])
        self.assertIn('annual_return', results['returns'])

    def test_analyze_risk(self):
        """测试风险分析"""
        # 运行回测
        self.engine.run()

        # 获取分析结果
        results = self.analyzer.analyze(self.engine.cerebro.runstrats[0][0])

        # 检查风险指标
        self.assertIn('sharpe', results)
        self.assertIn('drawdown', results)
        self.assertIn('max_drawdown', results['drawdown'])
        self.assertIn('max_drawdown_period', results['drawdown'])

    def test_analyze_trades(self):
        """测试交易分析"""
        # 运行回测
        self.engine.run()

        # 获取分析结果
        results = self.analyzer.analyze(self.engine.cerebro.runstrats[0][0])

        # 检查交易统计
        self.assertIn('trade', results)
        self.assertIn('total_trades', results['trade'])
        self.assertIn('win_rate', results['trade'])
        self.assertIn('avg_profit', results['trade'])
        self.assertIn('avg_loss', results['trade'])

    def test_plot_returns(self):
        """测试收益率绘图"""
        # 运行回测
        self.engine.run()

        # 测试绘图（这里只是测试是否抛出异常）
        try:
            self.analyzer.plot_returns(self.engine.cerebro.runstrats[0][0])
        except Exception as e:
            self.fail(f"绘图失败: {str(e)}")

if __name__ == '__main__':
    unittest.main()
