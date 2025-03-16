#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/3/16.
@author: Air.Zou
"""
import talib
import akshare as ak
import pandas as pd
import pyecharts
import streamlit as st
from streamlit_echarts import st_echarts
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
import numpy as np

st.title('股票K线图')

st.text_input('股票代码', key='code', placeholder='000001')
st.date_input('开始日期', key='start_date', value=pd.to_datetime('20210101'))
st.date_input('结束日期', key='end_date', value=pd.to_datetime('20241231'))

if st.session_state.code:
    stock = ak.stock_zh_a_hist(
        symbol=st.session_state.code,
        start_date=st.session_state.start_date.strftime('%Y%m%d'),
        end_date=st.session_state.end_date.strftime('%Y%m%d'), adjust="")

    stock.set_index('日期', inplace=True)
    stock['ma5'] = talib.MA(stock['收盘'], timeperiod=5)
    stock['ma10'] = talib.MA(stock['收盘'], timeperiod=10)
    stock['ma20'] = talib.MA(stock['收盘'], timeperiod=20)

    option1 = {
        "xAxis": {
            "type": "category",
            "data": stock.index.tolist(),
            "axisLabel": {"interval": "auto"},
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "type": "candlestick",
                "data": stock[['开盘', '收盘', '最低', '最高']].values.tolist(),
            },
            {
                "type": "line",
                "data": stock['ma5'].tolist(),
                "lineStyle": {"opacity": 0.5, "color": "blue"},
                "label": {"show": False},
            },
            {
                "type": "line",
                "data": stock['ma10'].tolist(),
                "lineStyle": {"opacity": 0.5, "color": "red"},
                "label": {"show": False},
            },
            {
                "type": "line",
                "data": stock['ma20'].tolist(),
                "lineStyle": {"opacity": 0.5, "color": "green"},
                "label": {"show": False},
            }
        ],
    }

    st_echarts(option1, height="500px")
