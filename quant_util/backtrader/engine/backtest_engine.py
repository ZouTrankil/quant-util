"""
回测引擎模块

提供回测的核心功能：
- 回测引擎初始化
- 数据加载
- 策略运行
- 结果分析
"""

import backtrader as bt
from datetime import datetime
from typing import List, Dict, Any, Optional

class BacktestEngine:
    """回测引擎类"""

    def __init__(self,
                 initial_cash: float = 100000.0,
                 commission: float = 0.001,
                 stake: int = 1,
                 slippage: float = 0.0):
        """
        初始化回测引擎

        Args:
            initial_cash: 初始资金
            commission: 手续费率
            stake: 每次交易数量
            slippage: 滑点
        """
        self.cerebro = bt.Cerebro()
        self.cerebro.broker.setcash(initial_cash)
        self.cerebro.broker.setcommission(commission=commission)
        self.cerebro.addsizer(bt.sizers.FixedSize, stake=stake)
        self.cerebro.broker.set_slippage_perc(slippage)

    def add_data(self,
                data: bt.feeds.PandasData,
                name: str = None) -> None:
        """
        添加数据到回测引擎

        Args:
            data: 回测数据
            name: 数据名称
        """
        self.cerebro.adddata(data, name=name)

    def add_strategy(self,
                    strategy: bt.Strategy,
                    **kwargs) -> None:
        """
        添加策略到回测引擎

        Args:
            strategy: 策略类
            **kwargs: 策略参数
        """
        self.cerebro.addstrategy(strategy, **kwargs)

    def add_analyzer(self,
                    analyzer: bt.Analyzer,
                    **kwargs) -> None:
        """
        添加分析器

        Args:
            analyzer: 分析器类
            **kwargs: 分析器参数
        """
        self.cerebro.addanalyzer(analyzer, **kwargs)

    def run(self) -> Dict[str, Any]:
        """
        运行回测

        Returns:
            Dict[str, Any]: 回测结果
        """
        results = self.cerebro.run()
        return self._process_results(results[0])

    def _process_results(self,
                        result: bt.Strategy) -> Dict[str, Any]:
        """
        处理回测结果

        Args:
            result: 策略实例

        Returns:
            Dict[str, Any]: 处理后的结果
        """
        return {
            'final_value': result.broker.getvalue(),
            'return': (result.broker.getvalue() / self.cerebro.broker.startingcash) - 1,
            'trades': len(result),
            'drawdown': result.analyzers.drawdown.get_analysis(),
            'sharpe': result.analyzers.sharpe.get_analysis(),
            'trade_analysis': result.analyzers.trade.get_analysis()
        }

    def plot(self) -> None:
        """绘制回测结果图表"""
        self.cerebro.plot()
