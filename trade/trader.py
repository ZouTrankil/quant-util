"""
交易接口模块

此模块定义了交易接口的基类和通用方法，提供统一的下单、撤单等操作。
不同的交易系统可以继承基类实现具体的交易逻辑。
"""

import abc
from typing import Dict, List, Optional, Any, Tuple, Union

from .models import Order, QuoteOnline
from utils.consts import OrderStatus, PriceType


class BaseTrader(abc.ABC):
    """交易接口基类

    定义了交易系统应有的基本功能，不同的交易系统应该继承该类并实现具体方法。
    """

    @abc.abstractmethod
    def query_asset(self) -> Dict[str, Any]:
        """查询账户资产

        Returns:
            Dict[str, Any]: 账户资产信息
        """
        pass

    @abc.abstractmethod
    def query_positions(self) -> List[Dict[str, Any]]:
        """查询持仓

        Returns:
            List[Dict[str, Any]]: 持仓信息列表
        """
        pass

    @abc.abstractmethod
    def query_orders(self, order_id: Optional[str] = None) -> List[Order]:
        """查询订单

        Args:
            order_id (Optional[str], optional): 订单号，为None时查询所有订单. 默认为None.

        Returns:
            List[Order]: 订单列表
        """
        pass

    @abc.abstractmethod
    def query_trades(self, order_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """查询成交

        Args:
            order_id (Optional[str], optional): 订单号，为None时查询所有成交. 默认为None.

        Returns:
            List[Dict[str, Any]]: 成交列表
        """
        pass

    @abc.abstractmethod
    def buy(
        self,
        stock_code: str,
        volume: int,
        price: float,
        price_type: Union[PriceType, int] = PriceType.LIMIT_PRICE,
        strategy_name: str = "",
        remark: str = ""
    ) -> int:
        """买入

        Args:
            stock_code (str): 证券代码
            volume (int): 委托数量(股)
            price (float): 委托价格
            price_type (Union[PriceType, int], optional): 价格类型. 默认为限价.
            strategy_name (str, optional): 策略名称. 默认为"".
            remark (str, optional): 备注. 默认为"".

        Returns:
            int: 订单编号，成功返回>0的值，失败返回-1
        """
        pass

    @abc.abstractmethod
    def sell(
        self,
        stock_code: str,
        volume: int,
        price: float,
        price_type: Union[PriceType, int] = PriceType.LIMIT_PRICE,
        strategy_name: str = "",
        remark: str = ""
    ) -> int:
        """卖出

        Args:
            stock_code (str): 证券代码
            volume (int): 委托数量(股)
            price (float): 委托价格
            price_type (Union[PriceType, int], optional): 价格类型. 默认为限价.
            strategy_name (str, optional): 策略名称. 默认为"".
            remark (str, optional): 备注. 默认为"".

        Returns:
            int: 订单编号，成功返回>0的值，失败返回-1
        """
        pass

    @abc.abstractmethod
    def cancel_order(self, order_id: int) -> bool:
        """撤单

        Args:
            order_id (int): 订单编号

        Returns:
            bool: 撤单请求是否成功
        """
        pass

    @abc.abstractmethod
    def subscribe_quote(self, stock_codes: List[str]) -> bool:
        """订阅行情

        Args:
            stock_codes (List[str]): 证券代码列表

        Returns:
            bool: 订阅请求是否成功
        """
        pass

    @abc.abstractmethod
    def unsubscribe_quote(self, stock_codes: List[str]) -> bool:
        """取消订阅行情

        Args:
            stock_codes (List[str]): 证券代码列表

        Returns:
            bool: 取消订阅请求是否成功
        """
        pass

    @abc.abstractmethod
    def get_quote(self, stock_code: str) -> Optional[QuoteOnline]:
        """获取实时行情

        Args:
            stock_code (str): 证券代码

        Returns:
            Optional[QuoteOnline]: 行情数据，失败返回None
        """
        pass

    def get_active_orders(self) -> List[Order]:
        """获取活跃订单列表（未完全成交且未撤销的订单）

        Returns:
            List[Order]: 活跃订单列表
        """
        all_orders = self.query_orders()
        active_status = [
            OrderStatus.SUBMITTED,
            OrderStatus.ACCEPTED,
            OrderStatus.PARTFILLED
        ]
        return [order for order in all_orders if order.order_status in active_status]

    def cancel_all_orders(self) -> Tuple[int, int]:
        """撤销所有活跃订单

        Returns:
            Tuple[int, int]: (成功撤单数, 失败撤单数)
        """
        active_orders = self.get_active_orders()
        success_count = 0
        failed_count = 0

        for order in active_orders:
            if self.cancel_order(order.order_id):
                success_count += 1
            else:
                failed_count += 1

        return success_count, failed_count

    def is_stock_tradable(self, stock_code: str) -> bool:
        """检查股票是否可交易

        Args:
            stock_code (str): 证券代码

        Returns:
            bool: 是否可交易
        """
        quote = self.get_quote(stock_code)
        if quote is None:
            return False

        # 检查是否处于交易状态
        tradable_status = [13]  # 连续交易状态
        return quote.stock_status in tradable_status
