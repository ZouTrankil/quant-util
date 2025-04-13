"""
可视化模块

提供回测结果可视化功能：
- 价格和指标图表
- 交易信号图表
- 资金曲线
- 回撤曲线
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, Any, List
import backtrader as bt

class BacktestPlotter:
    """回测结果绘图器"""

    def __init__(self,
                 style: str = 'seaborn',
                 figsize: tuple = (15, 10)):
        """
        初始化绘图器

        Args:
            style: 图表样式
            figsize: 图表大小
        """
        plt.style.use(style)
        self.figsize = figsize

    def plot_price_and_signals(self,
                             data: pd.DataFrame,
                             signals: pd.DataFrame,
                             indicators: Dict[str, pd.Series] = None) -> None:
        """
        绘制价格和信号图表

        Args:
            data: 价格数据
            signals: 交易信号
            indicators: 技术指标
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        # 绘制价格
        ax.plot(data.index, data['close'], label='Close Price')

        # 绘制买入信号
        buy_signals = signals[signals['signal'] == 1]
        ax.scatter(buy_signals.index,
                  data.loc[buy_signals.index, 'close'],
                  marker='^', color='g', label='Buy Signal')

        # 绘制卖出信号
        sell_signals = signals[signals['signal'] == -1]
        ax.scatter(sell_signals.index,
                  data.loc[sell_signals.index, 'close'],
                  marker='v', color='r', label='Sell Signal')

        # 绘制技术指标
        if indicators:
            for name, values in indicators.items():
                ax.plot(values.index, values, label=name)

        ax.set_title('Price and Trading Signals')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        plt.show()

    def plot_equity_curve(self,
                         equity: pd.Series,
                         benchmark: pd.Series = None) -> None:
        """
        绘制资金曲线

        Args:
            equity: 策略资金曲线
            benchmark: 基准资金曲线
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        # 绘制策略资金曲线
        ax.plot(equity.index, equity, label='Strategy')

        # 绘制基准资金曲线
        if benchmark is not None:
            ax.plot(benchmark.index, benchmark, label='Benchmark')

        ax.set_title('Equity Curve')
        ax.set_xlabel('Date')
        ax.set_ylabel('Equity')
        ax.legend()
        plt.show()

    def plot_drawdown(self,
                     drawdown: pd.Series) -> None:
        """
        绘制回撤曲线

        Args:
            drawdown: 回撤数据
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        ax.plot(drawdown.index, drawdown)
        ax.fill_between(drawdown.index, drawdown, 0, alpha=0.3)

        ax.set_title('Drawdown Curve')
        ax.set_xlabel('Date')
        ax.set_ylabel('Drawdown')
        plt.show()

    def plot_monthly_returns(self,
                           returns: pd.Series) -> None:
        """
        绘制月度收益率热力图

        Args:
            returns: 收益率数据
        """
        # 将收益率转换为月度数据
        monthly_returns = returns.resample('M').apply(lambda x: (1 + x).prod() - 1)

        # 创建月度收益率矩阵
        monthly_matrix = monthly_returns.unstack()

        fig, ax = plt.subplots(figsize=self.figsize)
        cax = ax.matshow(monthly_matrix, cmap='RdYlGn')

        # 设置坐标轴
        ax.set_xticks(range(len(monthly_matrix.columns)))
        ax.set_yticks(range(len(monthly_matrix.index)))
        ax.set_xticklabels(monthly_matrix.columns)
        ax.set_yticklabels(monthly_matrix.index)

        # 添加颜色条
        plt.colorbar(cax)

        ax.set_title('Monthly Returns Heatmap')
        plt.show()
