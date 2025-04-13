# Quant-Util

量化交易工具库，提供了常用的数据模型、工具函数和交易接口等功能。

## 特性

- 统一的行情数据模型 `QuoteOnline`
- 统一的订单数据模型 `Order`
- 股票代码格式化工具函数
- 涨跌停价格计算工具函数
- 日志记录功能
- 通用的交易接口定义
- 彩色控制台显示
- 格式化表格输出

## 安装

```bash
pip install quant-util
```

或者从源码安装：

```bash
git clone https://github.com/example/quant-util.git
cd quant-util
pip install -e .
```

## 快速开始

### 行情数据处理

```python
from trade.models import QuoteOnline
from display.console_display import print_quote_detail

# 创建行情数据对象
quote = QuoteOnline()
quote.stock_code = "600000"
quote.price = 10.5
quote.last_close = 10.0
quote.bid1 = 10.49
quote.bid_vol1 = 10000
quote.ask1 = 10.51
quote.ask_vol1 = 5000

# 打印行情数据
print_quote_detail(quote)
```

### 股票代码处理

```python
from utils.utils import (
    normalize_stock_code,
    format_stock_code_with_exchange,
    get_rise_limit_by_stock_code
)

# 规范化证券代码
code = normalize_stock_code("600000.SH")  # 返回 "600000"

# 添加交易所后缀
full_code = format_stock_code_with_exchange("600000")  # 返回 "600000.SH"

# 获取涨幅限制
limit = get_rise_limit_by_stock_code("600000")  # 返回 0.1 (10%)
```

### 日志记录

```python
from utils.logger import get_logger, set_log_config

# 设置日志配置
set_log_config(
    log_dir="./logs",
    app_name="my_app",
    console_level="INFO",
    file_level="DEBUG"
)

# 获取日志实例
logger = get_logger()

# 记录日志
logger.info("这是一条信息日志")
logger.debug("这是一条调试日志")
logger.warning("这是一条警告日志")
logger.error("这是一条错误日志")
```

### 交易接口

```python
from trade.trader import BaseTrader
from utils.consts import PriceType


# 实现自定义交易接口
class MyTrader(BaseTrader):
    # 实现抽象方法
    def query_asset(self):
        pass

    def query_positions(self):
        pass

    def query_orders(self, order_id=None):
        pass

    def query_trades(self, order_id=None):
        pass

    def buy(self, stock_code, volume, price, price_type=PriceType.LIMIT_PRICE, strategy_name="", remark=""):
        pass

    def sell(self, stock_code, volume, price, price_type=PriceType.LIMIT_PRICE, strategy_name="", remark=""):
        pass

    def cancel_order(self, order_id):
        pass

    def subscribe_quote(self, stock_codes):
        pass

    def unsubscribe_quote(self, stock_codes):
        pass

    def get_quote(self, stock_code):
        pass


# 使用交易接口
trader = MyTrader()
trader.buy("600000", 100, 10.5, PriceType.LIMIT_PRICE, "my_strategy", "测试下单")
```

## 模块结构

- `quant_util.core.models`: 数据模型定义
- `quant_util.core.utils`: 工具函数
- `quant_util.core.display`: 显示相关功能
- `quant_util.core.logger`: 日志功能
- `quant_util.core.trader`: 交易接口定义
- `quant_util.core.consts`: 常量定义

## 测试

运行测试：

```bash
python -m unittest discover -s tests
```

## 开发说明

从项目中提取代码到这个库：

1. 将通用代码模块化，移动到对应的目录结构中
2. 编写测试用例，确保代码质量
3. 更新文档和示例

## 许可证

MIT
