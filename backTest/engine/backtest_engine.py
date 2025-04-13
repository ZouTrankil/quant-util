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
from typing import List, Dict, Any, Optional, Union
import pandas as pd

class BacktestEngine:
    """回测引擎类"""

    def __init__(self,
                 initial_cash: float = 100000.0,
                 commission: float = 0.001,
                 stake: int = 1,
                 slippage: float = 0.0,
                 margin: float = 1.0):
        """
        初始化回测引擎

        Args:
            initial_cash: 初始资金
            commission: 手续费率
            stake: 每次交易数量
            slippage: 滑点
            margin: 保证金比例
        """
        self.cerebro = bt.Cerebro()
        self.cerebro.broker.setcash(initial_cash)
        self.cerebro.broker.setcommission(commission=commission)
        self.cerebro.addsizer(bt.sizers.FixedSize, stake=stake)
        self.cerebro.broker.set_slippage_perc(slippage)
        self.cerebro.broker.set_margin(margin)

        # 添加默认分析器
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        self.cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
        self.cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='time_return')
        self.cerebro.addanalyzer(bt.analyzers.VWR, _name='vwr')

    def add_data(self,
                data: Union[pd.DataFrame, bt.feeds.PandasData],
                name: str = None,
                timeframe: str = 'days',
                compression: int = 1) -> None:
        """
        添加数据到回测引擎

        Args:
            data: 回测数据，可以是DataFrame或PandasData对象
            name: 数据名称
            timeframe: 时间周期
            compression: 压缩周期
        """
        if isinstance(data, pd.DataFrame):
            data = bt.feeds.PandasData(
                dataname=data,
                timeframe=getattr(bt.TimeFrame, timeframe),
                compression=compression
            )
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

    def add_observer(self,
                    observer: bt.Observer,
                    **kwargs) -> None:
        """
        添加观察者

        Args:
            observer: 观察者类
            **kwargs: 观察者参数
        """
        self.cerebro.addobserver(observer, **kwargs)

    def set_sizer(self,
                 sizer: bt.Sizer,
                 **kwargs) -> None:
        """
        设置仓位管理器

        Args:
            sizer: 仓位管理器类
            **kwargs: 仓位管理器参数
        """
        self.cerebro.addsizer(sizer, **kwargs)

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
        # 获取分析器结果
        sharpe = result.analyzers.sharpe.get_analysis()
        drawdown = result.analyzers.drawdown.get_analysis()
        trades = result.analyzers.trades.get_analysis()
        returns = result.analyzers.returns.get_analysis()
        time_return = result.analyzers.time_return.get_analysis()
        vwr = result.analyzers.vwr.get_analysis()

        return {
            'final_value': result.broker.getvalue(),
            'return': returns.get('rtot', 0),
            'annual_return': returns.get('ravg', 0),
            'sharpe_ratio': sharpe.get('sharperatio', 0),
            'max_drawdown': drawdown.get('max', {}).get('drawdown', 0),
            'max_drawdown_len': drawdown.get('max', {}).get('len', 0),
            'total_trades': trades.get('total', {}).get('total', 0),
            'won_trades': trades.get('won', {}).get('total', 0),
            'lost_trades': trades.get('lost', {}).get('total', 0),
            'win_rate': trades.get('won', {}).get('total', 0) / trades.get('total', {}).get('total', 1),
            'vwr': vwr.get('vwr', 0),
            'time_returns': time_return
        }

    def plot(self, style: str = 'candlestick', volume: bool = True) -> None:
        """
        绘制回测结果图表

        Args:
            style: 图表样式
            volume: 是否显示成交量
        """
        self.cerebro.plot(style=style, volume=volume)
