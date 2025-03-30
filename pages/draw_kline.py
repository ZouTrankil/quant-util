#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/3/16.
@author: Air.Zou
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import talib
import pandas as pd
import pyecharts
import streamlit as st
from streamlit_echarts import st_echarts
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
import numpy as np
from utils.global_config import DataSource
from utils.code_symbol import code_symbol

st.title('股票K线图')

st.text_input('股票代码', key='code', placeholder='000001')
st.date_input('开始日期', key='start_date', value=pd.to_datetime('20250101'))
st.date_input('结束日期', key='end_date', value=pd.to_datetime('20251231'))

if st.session_state.code:
    code = st.session_state.code
    code = code_symbol(code)
    start_date = st.session_state.start_date.strftime('%Y%m%d')
    end_date = st.session_state.end_date.strftime('%Y%m%d')
    pro = DataSource.tushare_pro
    stock = pro.daily(ts_code=code, start_date=start_date
                                         , end_date=end_date)

    stock.set_index('trade_date', inplace=True)
    stock.sort_index(inplace=True)

    # 计算均线，使用min_periods参数避免开始的NaN值，并保留2位小数
    stock['ma5'] = stock['close'].rolling(window=5, min_periods=1).mean().round(3)
    stock['ma10'] = stock['close'].rolling(window=10, min_periods=1).mean().round(3)
    stock['ma20'] = stock['close'].rolling(window=20, min_periods=1).mean().round(3)

    # 格式化日期显示
    dates = [pd.to_datetime(d).strftime('%Y-%m-%d') for d in stock.index]

    option1 = {
        "title": {"text": f"{st.session_state.code} 股票K线图"},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross"},
        },
        "legend": {
            "data": ["K线", "MA5", "MA10", "MA20"],
            "top": "3%"
        },
        "grid": {
            "left": "10%",
            "right": "10%",
            "bottom": "15%"
        },
        "xAxis": {
            "type": "category",
            "data": dates,
            "scale": True,
            "boundaryGap": False,
            "axisLine": {"onZero": False},
            "axisLabel": {
                "formatter": "{value}",
                "rotate": 45
            },
            "splitLine": {"show": False},
            "min": "dataMin",
            "max": "dataMax"
        },
        "yAxis": {
            "type": "value",
            "scale": True,
            "splitLine": {"show": True},
            "splitArea": {"show": True}
        },
        "dataZoom": [
            {
                "type": "inside",
                "start": 50,
                "end": 100
            },
            {
                "show": True,
                "type": "slider",
                "bottom": "5%",
                "start": 50,
                "end": 100
            }
        ],
        "series": [
            {
                "name": "K线",
                "type": "candlestick",
                "data": stock[['open', 'close', 'low', 'high']].values.tolist(),
                "itemStyle": {
                    "color": "#ef232a",
                    "color0": "#14b143",
                    "borderColor": "#ef232a",
                    "borderColor0": "#14b143"
                },
            },
            {
                "name": "MA5",
                "type": "line",
                "data": stock['ma5'].tolist(),
                "smooth": True,
                "lineStyle": {"opacity": 0.5, "color": "#ffd700"},
                "label": {"show": False},
            },
            {
                "name": "MA10",
                "type": "line",
                "data": stock['ma10'].tolist(),
                "smooth": True,
                "lineStyle": {"opacity": 0.5, "color": "#ff69b4"},
                "label": {"show": False},
            },
            {
                "name": "MA20",
                "type": "line",
                "data": stock['ma20'].tolist(),
                "smooth": True,
                "lineStyle": {"opacity": 0.5, "color": "#87ceeb"},
                "label": {"show": False},
            }
        ],
    }

    st_echarts(option1, height="600px")
