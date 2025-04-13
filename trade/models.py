"""
数据模型定义模块

此模块包含了量化交易系统中使用的各种数据模型定义，如行情数据、订单数据等。
"""

import datetime
import json
from typing import Dict, Optional, List, Any


class QuoteOnline:
    """实时行情数据模型

    封装了股票实时行情的完整数据，包括价格、成交量、买卖盘等信息。
    """

    def __init__(self) -> None:
        """初始化行情数据对象"""
        self.stock_code = ""  # 证券代码
        self.datetime = ""    # 行情时间(包含日期)
        self.time = ""        # 行情时间
        self.price = 0.0      # 最新价格
        self.open = 0.0       # 开盘价
        self.high = 0.0       # 最高价
        self.low = 0.0        # 最低价
        self.last_close = 0.0 # 昨收
        self.amount = 0.0     # 总成交额
        self.volume = 0       # 总成交量（股）

        # 卖盘价格
        self.ask1 = 0.0       # 卖一价
        self.ask2 = 0.0       # 卖二价
        self.ask3 = 0.0       # 卖三价
        self.ask4 = 0.0       # 卖四价
        self.ask5 = 0.0       # 卖五价

        # 卖盘量（股）
        self.ask_vol1 = 0     # 卖一量
        self.ask_vol2 = 0     # 卖二量
        self.ask_vol3 = 0     # 卖三量
        self.ask_vol4 = 0     # 卖四量
        self.ask_vol5 = 0     # 卖五量

        # 买盘价格
        self.bid1 = 0.0       # 买一价
        self.bid2 = 0.0       # 买二价
        self.bid3 = 0.0       # 买三价
        self.bid4 = 0.0       # 买四价
        self.bid5 = 0.0       # 买五价

        # 买盘量（股）
        self.bid_vol1 = 0     # 买一量
        self.bid_vol2 = 0     # 买二量
        self.bid_vol3 = 0     # 买三量
        self.bid_vol4 = 0     # 买四量
        self.bid_vol5 = 0     # 买五量

        self.stock_status = 0  # 证券状态

    def to_dict(self) -> Dict[str, Any]:
        """将对象转换为字典格式

        Returns:
            Dict[str, Any]: 包含所有属性的字典
        """
        result = {}
        attrs = list(filter(
            lambda s: not s.startswith("__") and not callable(getattr(self, s)),
            dir(self)
        ))
        for attr in attrs:
            result[attr] = getattr(self, attr)
        return result

    def __str__(self) -> str:
        """字符串表示

        Returns:
            str: JSON格式的字符串表示
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def load_from_dict(cls, stock_code: str, data: Dict[str, Any]) -> Optional["QuoteOnline"]:
        """从字典数据加载行情对象

        Args:
            stock_code (str): 股票代码
            data (Dict[str, Any]): 原始行情数据字典

        Returns:
            Optional[QuoteOnline]: 行情对象，如果加载失败则返回None
        """
        if data is None:
            return None

        quote = QuoteOnline()
        quote.stock_code = stock_code

        # 处理时间
        if "time" in data:
            timestamp = data.get("time", 0) / 1000
            dt = datetime.datetime.fromtimestamp(timestamp)
            quote.datetime = dt.strftime("%Y-%m-%d %H:%M:%S")
            quote.time = dt.strftime("%H:%M:%S")

        # 基本价格信息
        quote.price = data.get("lastPrice", 0.0)
        quote.open = data.get("open", 0.0)
        quote.high = data.get("high", 0.0)
        quote.low = data.get("low", 0.0)
        quote.last_close = data.get("lastClose", 0.0)
        quote.amount = data.get("amount", 0.0)
        quote.volume = data.get("volume", 0) * 100  # 成交量转换为股

        # 卖盘价格
        ask_prices = data.get("askPrice", [0, 0, 0, 0, 0])
        if isinstance(ask_prices, List) and len(ask_prices) >= 5:
            quote.ask1, quote.ask2, quote.ask3, quote.ask4, quote.ask5 = ask_prices[:5]

        # 卖盘量
        ask_vols = data.get("askVol", [0, 0, 0, 0, 0])
        if isinstance(ask_vols, List) and len(ask_vols) >= 5:
            quote.ask_vol1 = ask_vols[0] * 100
            quote.ask_vol2 = ask_vols[1] * 100
            quote.ask_vol3 = ask_vols[2] * 100
            quote.ask_vol4 = ask_vols[3] * 100
            quote.ask_vol5 = ask_vols[4] * 100

        # 买盘价格
        bid_prices = data.get("bidPrice", [0, 0, 0, 0, 0])
        if isinstance(bid_prices, List) and len(bid_prices) >= 5:
            quote.bid1, quote.bid2, quote.bid3, quote.bid4, quote.bid5 = bid_prices[:5]

        # 买盘量
        bid_vols = data.get("bidVol", [0, 0, 0, 0, 0])
        if isinstance(bid_vols, List) and len(bid_vols) >= 5:
            quote.bid_vol1 = bid_vols[0] * 100
            quote.bid_vol2 = bid_vols[1] * 100
            quote.bid_vol3 = bid_vols[2] * 100
            quote.bid_vol4 = bid_vols[3] * 100
            quote.bid_vol5 = bid_vols[4] * 100

        quote.stock_status = data.get("stockStatus", 0)

        return quote


class Order:
    """订单数据模型

    封装了交易订单的完整信息。
    """

    def __init__(self) -> None:
        """初始化订单对象"""
        self.account_id = ""         # 账户ID
        self.account_type = 0        # 账户类型
        self.account_type_name = ""  # 账户类型名称
        self.direction = 0           # 买卖方向
        self.direction_name = ""     # 买卖方向名称
        self.offset_flag = 0         # 开平标志
        self.offset_flag_name = ""   # 开平标志名称
        self.order_id = 0            # 订单编号
        self.order_remark = ""       # 订单备注
        self.order_status = 0        # 订单状态
        self.order_status_name = ""  # 订单状态名称
        self.order_sysid = ""        # 系统编号
        self.order_time = 0          # 下单时间
        self.order_type = 0          # 订单类型
        self.order_type_name = ""    # 订单类型名称
        self.order_volume = 0        # 委托数量
        self.price = 0.0             # 委托价格
        self.price_type = 0          # 价格类型
        self.price_type_name = ""    # 价格类型名称
        self.status_msg = ""         # 状态信息
        self.stock_code = ""         # 证券代码
        self.strategy_name = ""      # 策略名称
        self.traded_price = 0.0      # 成交价格
        self.traded_volume = 0       # 成交数量

    def to_dict(self) -> Dict[str, Any]:
        """将对象转换为字典格式

        Returns:
            Dict[str, Any]: 包含所有属性的字典
        """
        result = {}
        attrs = list(filter(
            lambda s: not s.startswith("__") and not callable(getattr(self, s)),
            dir(self)
        ))
        for attr in attrs:
            result[attr] = getattr(self, attr)
        return result

    def __str__(self) -> str:
        """字符串表示

        Returns:
            str: JSON格式的字符串表示
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def load_from_dict(cls, data: Dict[str, Any]) -> Optional["Order"]:
        """从字典数据加载订单对象

        Args:
            data (Dict[str, Any]): 订单数据字典

        Returns:
            Optional[Order]: 订单对象，如果加载失败则返回None
        """
        if data is None:
            return None

        order = Order()
        # 映射属性
        for key, value in data.items():
            if hasattr(order, key):
                setattr(order, key, value)

        return order
