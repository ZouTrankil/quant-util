"""
基础策略模块

提供策略开发的基础类：
- 策略基类
- 常用指标
- 信号生成
- 仓位管理
"""

import backtrader as bt
from typing import Dict, Any, Optional

class BaseStrategy(bt.Strategy):
    """基础策略类"""

    params = (
        ('printlog', False),
    )

    def __init__(self):
        """初始化策略"""
        super().__init__()
        self.order = None
        self.buyprice = None
        self.buycomm = None

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
                    f'成本={order.executed.value:.2f}, '
                    f'手续费={order.executed.comm:.2f}'
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(
                    f'卖出: 价格={order.executed.price:.2f}, '
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
