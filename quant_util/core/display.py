"""
显示模块

该模块提供与数据展示相关的工具函数，如彩色输出、表格显示等。
"""

from typing import Optional, List, Dict, Any, Union
import json
from colorama import Fore, Style, init
from terminaltables3 import AsciiTable

from .models import QuoteOnline
from .utils import get_number_desc, calculate_change_percent

# 初始化colorama
init()


def colored_value(value: float, compare_to: float, suffix: str = "") -> str:
    """根据与基准值的比较给数值着色

    Args:
        value (float): 要显示的数值
        compare_to (float): 比较基准值
        suffix (str, optional): 后缀，如"%". 默认为"".

    Returns:
        str: 带颜色的字符串
    """
    formatted = f"{round(value, 2)}{suffix}"

    if value == compare_to:
        return formatted
    elif value > compare_to:
        return f"{Fore.RED}{formatted}{Style.RESET_ALL}"
    else:
        return f"{Fore.GREEN}{formatted}{Style.RESET_ALL}"


def blue_text(text: str) -> str:
    """蓝色文本

    Args:
        text (str): 要着色的文本

    Returns:
        str: 蓝色文本
    """
    return f"{Fore.BLUE}{text}{Style.RESET_ALL}"


def yellow_text(text: str) -> str:
    """黄色文本

    Args:
        text (str): 要着色的文本

    Returns:
        str: 黄色文本
    """
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"


def magenta_text(text: str) -> str:
    """洋红色文本

    Args:
        text (str): 要着色的文本

    Returns:
        str: 洋红色文本
    """
    return f"{Fore.MAGENTA}{text}{Style.RESET_ALL}"


def red_text(text: str) -> str:
    """红色文本

    Args:
        text (str): 要着色的文本

    Returns:
        str: 红色文本
    """
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


def green_text(text: str) -> str:
    """绿色文本

    Args:
        text (str): 要着色的文本

    Returns:
        str: 绿色文本
    """
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"


def format_quote_simple(quote: QuoteOnline) -> str:
    """格式化行情数据的简要信息

    Args:
        quote (QuoteOnline): 行情数据对象

    Returns:
        str: 格式化后的字符串
    """
    change_pct = calculate_change_percent(quote.price, quote.last_close)
    change_str = colored_value(change_pct, 0, "%")

    message = (
        f"证券代码: {blue_text(quote.stock_code)}, "
        f"行情时间: {yellow_text(quote.time)}, "
        f"现价: {colored_value(quote.price, quote.last_close)}, "
        f"涨幅: {change_str}, "
        f"总量: {yellow_text(get_number_desc(round(quote.volume / 100, 0)))}, "
        f"总额: {magenta_text(get_number_desc(round(quote.amount, 2)))}"
    )
    return message


def print_quote_simple(quote: Optional[QuoteOnline]) -> None:
    """打印行情数据的简要信息

    Args:
        quote (Optional[QuoteOnline]): 行情数据对象
    """
    if quote is not None:
        print(format_quote_simple(quote))


def print_quote_detail(quote: Optional[QuoteOnline]) -> None:
    """打印行情数据的详细信息，包括五档盘口

    Args:
        quote (Optional[QuoteOnline]): 行情数据对象
    """
    if quote is None:
        return

    table_data = []

    # 基本信息
    table_data.append([
        "现价",
        colored_value(quote.price, quote.last_close),
        "涨幅",
        colored_value(calculate_change_percent(quote.price, quote.last_close), 0, "%"),
    ])

    table_data.append([
        "最高",
        colored_value(round(quote.high, 2), quote.last_close),
        "最低",
        colored_value(round(quote.low, 2), quote.last_close),
    ])

    table_data.append(["昨收", round(quote.last_close, 2), "", ""])

    table_data.append([
        "总量",
        yellow_text(get_number_desc(round(quote.volume / 100, 0))),
        "总额",
        magenta_text(get_number_desc(round(quote.amount, 2))),
    ])

    # 分隔线和表头
    table_data.append(["-" * 10, "-" * 10, "-" * 10, "-" * 10])
    table_data.append(["", "报价", "挂单量(手)", "挂单总金额"])
    table_data.append(["-" * 10, "-" * 10, "-" * 10, "-" * 10])

    # 卖盘
    table_data.append([
        "卖五",
        colored_value(round(quote.ask5, 2), quote.last_close),
        yellow_text(str(int(round(quote.ask_vol5 / 100, 0)))),
        magenta_text(get_number_desc(quote.ask5 * quote.ask_vol5)),
    ])

    table_data.append([
        "卖四",
        colored_value(round(quote.ask4, 2), quote.last_close),
        yellow_text(str(int(round(quote.ask_vol4 / 100, 0)))),
        magenta_text(get_number_desc(quote.ask4 * quote.ask_vol4)),
    ])

    table_data.append([
        "卖三",
        colored_value(round(quote.ask3, 2), quote.last_close),
        yellow_text(str(int(round(quote.ask_vol3 / 100, 0)))),
        magenta_text(get_number_desc(quote.ask3 * quote.ask_vol3)),
    ])

    table_data.append([
        "卖二",
        colored_value(round(quote.ask2, 2), quote.last_close),
        yellow_text(str(int(round(quote.ask_vol2 / 100, 0)))),
        magenta_text(get_number_desc(quote.ask2 * quote.ask_vol2)),
    ])

    table_data.append([
        "卖一",
        colored_value(round(quote.ask1, 2), quote.last_close),
        yellow_text(str(int(round(quote.ask_vol1 / 100, 0)))),
        magenta_text(get_number_desc(quote.ask1 * quote.ask_vol1)),
    ])

    # 分隔线
    table_data.append(["-" * 10, "-" * 10, "-" * 10, "-" * 10])

    # 买盘
    table_data.append([
        "买一",
        colored_value(round(quote.bid1, 2), quote.last_close),
        yellow_text(str(int(round(quote.bid_vol1 / 100, 0)))),
        magenta_text(get_number_desc(quote.bid1 * quote.bid_vol1)),
    ])

    table_data.append([
        "买二",
        colored_value(round(quote.bid2, 2), quote.last_close),
        yellow_text(str(int(round(quote.bid_vol2 / 100, 0)))),
        magenta_text(get_number_desc(quote.bid2 * quote.bid_vol2)),
    ])

    table_data.append([
        "买三",
        colored_value(round(quote.bid3, 2), quote.last_close),
        yellow_text(str(int(round(quote.bid_vol3 / 100, 0)))),
        magenta_text(get_number_desc(quote.bid3 * quote.bid_vol3)),
    ])

    table_data.append([
        "买四",
        colored_value(round(quote.bid4, 2), quote.last_close),
        yellow_text(str(int(round(quote.bid_vol4 / 100, 0)))),
        magenta_text(get_number_desc(quote.bid4 * quote.bid_vol4)),
    ])

    table_data.append([
        "买五",
        colored_value(round(quote.bid5, 2), quote.last_close),
        yellow_text(str(int(round(quote.bid_vol5 / 100, 0)))),
        magenta_text(get_number_desc(quote.bid5 * quote.bid_vol5)),
    ])

    # 创建表格
    table = AsciiTable(table_data)
    table.inner_heading_row_border = False
    table.title = f" {yellow_text(quote.stock_code)} - {yellow_text(quote.datetime)}"

    print(table.table)


def print_dict_as_table(data: Dict[str, Any], title: str = "") -> None:
    """将字典打印为表格

    Args:
        data (Dict[str, Any]): 字典数据
        title (str, optional): 表格标题. 默认为"".
    """
    table_data = []

    # 添加表头
    table_data.append(["键", "值"])

    # 添加数据行
    for key, value in data.items():
        # 处理嵌套字典或列表
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        table_data.append([key, value])

    # 创建表格
    table = AsciiTable(table_data)
    if title:
        table.title = title

    print(table.table)


def print_list_as_table(data: List[Dict[str, Any]], columns: Optional[List[str]] = None, title: str = "") -> None:
    """将字典列表打印为表格

    Args:
        data (List[Dict[str, Any]]): 字典列表数据
        columns (Optional[List[str]], optional): 要显示的列名. 默认为None(显示所有列).
        title (str, optional): 表格标题. 默认为"".
    """
    if not data:
        print("没有数据")
        return

    # 如果没有指定列名，使用第一个字典的所有键
    if columns is None:
        columns = list(data[0].keys())

    table_data = []

    # 添加表头
    table_data.append(columns)

    # 添加数据行
    for item in data:
        row = []
        for col in columns:
            value = item.get(col, "")
            # 处理嵌套字典或列表
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            row.append(value)
        table_data.append(row)

    # 创建表格
    table = AsciiTable(table_data)
    if title:
        table.title = title

    print(table.table)
