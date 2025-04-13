"""
常量定义模块

此模块包含了量化交易系统中使用的各种常量定义。
"""

from enum import Enum, IntEnum


class StockStatus(IntEnum):
    """股票交易状态枚举"""
    UNKNOWN = 0          # 未知状态
    UNKNOWN_10 = 10      # 未知状态
    BEFORE_OPEN = 11     # 开盘前
    CALL_AUCTION = 12    # 集合竞价时段
    CONTINUOUS_TRADE = 13  # 连续交易
    MARKET_CLOSED = 14    # 休市
    END_OF_DAY = 15      # 闭市
    VOLATILITY_INTERRUPTION = 16  # 波动性中断
    TEMP_SUSPENSION = 17  # 临时停牌
    CLOSING_CALL_AUCTION = 18  # 收盘集合竞价
    MIDDAY_CALL_AUCTION = 19  # 盘中集合竞价
    SUSPENDED_UNTIL_CLOSE = 20  # 暂停交易至闭市
    FIELD_ERROR = 21     # 获取字段异常
    AFTER_HOURS_FIXED = 22  # 盘后固定价格行情
    AFTER_HOURS_FIXED_END = 23  # 盘后固定价格行情完毕


class OrderDirection(IntEnum):
    """订单买卖方向枚举"""
    BUY = 1              # 买入
    SELL = 2             # 卖出


class OrderStatus(IntEnum):
    """订单状态枚举"""
    SUBMITTED = 1        # 已报
    ACCEPTED = 2         # 已报待撤
    PARTFILLED = 3       # 部成
    FILLED = 4           # 全成
    CANCELLED = 5        # 已撤
    REJECTED = 6         # 废单
    UNKNOWN = 7          # 未知


class OrderType(IntEnum):
    """订单类型枚举"""
    NORMAL = 0           # 普通单
    MARKET = 1           # 市价单


class PriceType(IntEnum):
    """价格类型枚举"""
    LIMIT_PRICE = 1                   # 限价
    BEST_OR_CANCEL = 2                # 最优五档即时成交剩余撤销
    BEST_OR_LIMIT = 3                 # 最优五档即时成交剩余转限价
    ALL_OR_CANCEL = 4                 # 五档即时全额成交或撤销
    FORWARD_BEST = 5                  # 本方最优
    REVERSE_BEST_OR_LIMIT = 6         # 对手方最优
    MARKET_TO_LIMIT = 7               # 最优五档市价
    LIMIT_TO_LIMIT = 8                # 限价盘
    MARKET_TO_MARKET = 9              # 市价盘
    FIX_PRICE_TO_LIMIT = 10           # 定价盘
    MARKET_OR_LIMIT = 11              # 市价剩余转限价
    LIMIT_OR_CANCEL = 12              # 限价立即成交剩余撤销


class OffsetFlag(IntEnum):
    """开平标志枚举"""
    OPEN = 0             # 开仓
    CLOSE = 1            # 平仓
    FORCE_CLOSE = 2      # 强平
    CLOSE_TODAY = 3      # 平今
    CLOSE_YESTERDAY = 4  # 平昨
    FORCE_OFF = 5        # 强减
    LOCAL_FORCE_CLOSE = 6  # 本地强平


class ExchangeType(str, Enum):
    """交易所类型枚举"""
    SH = "SH"            # 上海证券交易所
    SZ = "SZ"            # 深圳证券交易所
    BJ = "BJ"            # 北京证券交易所


class AccountType(str, Enum):
    """账户类型枚举"""
    STOCK = "STOCK"      # 股票账户
    FUTURE = "FUTURE"    # 期货账户
    OPTION = "OPTION"    # 期权账户
