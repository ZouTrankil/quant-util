#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/3/26.
@author: Air.Zou
"""
__doc__ = """
基础数据获取
stock_basic

输入参数

名称	类型	必选	描述
ts_code	str	N	TS股票代码
name	str	N	名称
market	str	N	市场类别 （主板/创业板/科创板/CDR/北交所）
list_status	str	N	上市状态 L上市 D退市 P暂停上市，默认是L
exchange	str	N	交易所 SSE上交所 SZSE深交所 BSE北交所
is_hs	str	N	是否沪深港通标的，N否 H沪股通 S深股通
输出参数

名称	类型	默认显示	描述
ts_code	str	Y	TS代码
symbol	str	Y	股票代码
name	str	Y	股票名称
area	str	Y	地域
industry	str	Y	所属行业
fullname	str	N	股票全称
enname	str	N	英文全称
cnspell	str	Y	拼音缩写
market	str	Y	市场类型（主板/创业板/科创板/CDR）
exchange	str	N	交易所代码
curr_type	str	N	交易货币
list_status	str	N	上市状态 L上市 D退市 P暂停上市
list_date	str	Y	上市日期
delist_date	str	N	退市日期
is_hs	str	N	是否沪深港通标的，N否 H沪股通 S深股通
act_name	str	Y	实控人名称
act_ent_type	str	Y	实控人企业性质


"""

from data.tushare.basic.exchange_calendar import get_trade_days_str

basic_exchange_date = get_trade_days_str()