#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 27/02/2025.
@author: Air.Zou
"""
def code_symbol(code):
    if type(code) == int:
        # 填充为6位
        code = str(code).zfill(6)
    # 定义一个字典，存储不同前缀对应的交易所后缀
    exchange_suffix = {
        '00': '.SZ',
        '30': '.SZ',
        '60': '.SH',
        '68': '.SH',  # 科创板，上海证券交易所
        '90': '.SH',
        '11': '.SH',
        '4': '.BJ',  # 北京证券交易所，以 4 开头
        '8': '.BJ'  # 北京证券交易所，以 8 开头
    }
    # 遍历字典的键
    for prefix, suffix in exchange_suffix.items():
        if code.startswith(prefix):
            return code + suffix
    # 如果没有匹配到任何前缀，返回 None
    return None
