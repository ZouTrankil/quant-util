"""
基础策略模块

提供策略开发的基础类：
- 策略基类
- 常用指标
- 信号生成
- 仓位管理
"""

import backtrader as bt
from typing import Dict, Any, Optional, List
import numpy as np

class BaseStrategy(bt.Strategy):
    """基础策略类"""

    params = (
        ('printlog', False),
        ('risk_free_rate', 0.02),  # 无风险利率
        ('position_size', 1),      # 默认仓位大小
        ('stop_loss', 0.02),      # 止损比例
        ('take_profit', 0.05),    # 止盈比例
    )

    def __init__(self):
        """初始化策略"""
        super().__init__()
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # 记录交易状态
        self.trade_history = []
        self.current_position = None

        # 初始化技术指标
        self._init_indicators()

    def _init_indicators(self):
        """初始化技术指标"""
        # 移动平均线
        self.sma20 = bt.indicators.SimpleMovingAverage(self.data, period=20)
        self.sma50 = bt.indicators.SimpleMovingAverage(self.data, period=50)

        # MACD
        self.macd = bt.indicators.MACD(self.data)

        # RSI
        self.rsi = bt.indicators.RSI(self.data, period=14)

        # 布林带
        self.boll = bt.indicators.BollingerBands(self.data, period=20)

        # ATR
        self.atr = bt.indicators.ATR(self.data, period=14)

    def log(self, txt: str, dt: Optional[Any] = None, doprint: bool = False) -> None:
        """
        记录日志

        Args:
            txt: 日志内容
            dt: 日期时间
            doprint: 是否打印
        """
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()} {txt}')

    def notify_order(self, order) -> None:
        """
        订单状态通知

        Args:
            order: 订单对象
        """
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'买入: 价格={order.executed.price:.2f}, '
                    f'数量={order.executed.size}, '
                    f'成本={order.executed.value:.2f}, '
                    f'手续费={order.executed.comm:.2f}'
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

                # 设置止损止盈
                stop_price = self.buyprice * (1 - self.params.stop_loss)
                take_profit_price = self.buyprice * (1 + self.params.take_profit)
                self.sell(exectype=bt.Order.Stop, price=stop_price)
                self.sell(exectype=bt.Order.Limit, price=take_profit_price)

            else:
                self.log(
                    f'卖出: 价格={order.executed.price:.2f}, '
                    f'数量={order.executed.size}, '
                    f'成本={order.executed.value:.2f}, '
                    f'手续费={order.executed.comm:.2f}'
                )

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单取消/保证金不足/拒绝')

        self.order = None

    def notify_trade(self, trade) -> None:
        """
        交易通知

        Args:
            trade: 交易对象
        """
        if not trade.isclosed:
            return

        # 记录交易历史
        self.trade_history.append({
            'entry_date': bt.num2date(trade.dtopen),
            'exit_date': bt.num2date(trade.dtclose),
            'entry_price': trade.price,
            'exit_price': trade.pnlcomm / trade.size + trade.price,
            'size': trade.size,
            'pnl': trade.pnl,
            'pnlcomm': trade.pnlcomm,
            'commission': trade.commission
        })

        self.log(f'交易利润: 毛利润={trade.pnl:.2f}, 净利润={trade.pnlcomm:.2f}')

    def next(self) -> None:
        """
        策略逻辑
        需要在子类中实现
        """
        raise NotImplementedError("请在子类中实现next方法")

    def stop(self) -> None:
        """
        策略结束
        """
        self.log(f'期末资金: {self.broker.getvalue():.2f}')

        # 计算策略统计指标
        if self.trade_history:
            self._calculate_statistics()

    def _calculate_statistics(self) -> None:
        """计算策略统计指标"""
        trades = self.trade_history
        pnls = [t['pnlcomm'] for t in trades]

        # 计算收益率序列
        returns = np.array(pnls) / self.broker.startingcash

        # 计算年化收益率
        total_days = (trades[-1]['exit_date'] - trades[0]['entry_date']).days
        annual_return = (1 + sum(returns)) ** (365 / total_days) - 1

        # 计算夏普比率
        sharpe = (np.mean(returns) - self.params.risk_free_rate/252) / np.std(returns) * np.sqrt(252)

        # 计算最大回撤
        cummax = np.maximum.accumulate(np.cumsum(returns))
        drawdown = (cummax - np.cumsum(returns)) / cummax
        max_drawdown = np.max(drawdown)

        self.log(f'策略统计:')
        self.log(f'总交易次数: {len(trades)}')
        self.log(f'年化收益率: {annual_return:.2%}')
        self.log(f'夏普比率: {sharpe:.2f}')
        self.log(f'最大回撤: {max_drawdown:.2%}')
        self.log(f'胜率: {len([t for t in trades if t["pnlcomm"] > 0]) / len(trades):.2%}')
