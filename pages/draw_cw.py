# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import pandas as pd
import tushare as ts
import plotly.express as px
from datetime import datetime
from utils import DataSource
# 初始化Tushare
pro = DataSource.tushare_pro

# 核心财务指标列表
CORE_INDICATORS = {
    'eps': '每股收益',
    'dt_eps': '稀释每股收益',
    'total_revenue_ps': '每股营业总收入',
    'revenue_ps': '每股营业收入',
    'grossprofit_margin': '毛利率',
    'netprofit_margin': '净利润率',
    'roe': '净资产收益率',
    'debt_to_assets': '资产负债率',
    'current_ratio': '流动比率',
    'quick_ratio': '速动比率'
}

# 所有可用指标（部分示例，可根据需要扩展）
ALL_INDICATORS = {
    'eps': '每股收益',
    'dt_eps': '稀释每股收益',
    'total_revenue_ps': '每股营业总收入',
    'revenue_ps': '每股营业收入',
    'capital_rese_ps': '每股资本公积',
    'surplus_rese_ps': '每股盈余公积',
    'grossprofit_margin': '毛利率',
    'netprofit_margin': '净利润率',
    'roe': '净资产收益率',
    'debt_to_assets': '资产负债率',
    'current_ratio': '流动比率',
    'quick_ratio': '速动比率',
    # 可根据文档添加更多指标
}

def fetch_fina_data(ts_code):
    """获取财务指标数据"""
    try:
        df = pro.fina_indicator(ts_code=ts_code)
        # 处理日期格式
        df['end_date'] = pd.to_datetime(df['end_date'])
        df['year'] = df['end_date'].dt.year
        df['quarter'] = df['end_date'].dt.quarter
        return df
    except Exception as e:
        st.error(f"数据获取失败: {str(e)}")
        return None

def create_yearly_analysis(df, indicators):
    """创建年度分析"""
    yearly_data = df.groupby('year')[list(indicators.keys())].mean().reset_index()
    return yearly_data

def create_quarterly_analysis(df, indicators):
    """创建季度分析"""
    quarterly_data = df.groupby(['year', 'quarter'])[list(indicators.keys())].mean().reset_index()
    quarterly_data['period'] = quarterly_data['year'].astype(str) + 'Q' + quarterly_data['quarter'].astype(str)
    return quarterly_data

def plot_indicator(df, x_col, y_col, title, indicator_name):
    """绘制指标图表"""
    fig = px.line(df, x=x_col, y=y_col,
                 title=f"{indicator_name} - {title}",
                 labels={x_col: '时间', y_col: indicator_name})
    return fig

# Streamlit界面
st.title("上市公司财务指标分析")

# 侧边栏输入
st.sidebar.header("设置")
ts_code = st.sidebar.text_input("请输入股票代码（如600000.SH）", "600000.SH")
show_all_indicators = st.sidebar.checkbox("显示所有指标", False)

# 选择要展示的指标
indicators = ALL_INDICATORS if show_all_indicators else CORE_INDICATORS
selected_indicators = st.sidebar.multiselect(
    "选择要分析的指标",
    options=list(indicators.keys()),
    default=list(indicators.keys())[:5],  # 默认显示前5个指标
    format_func=lambda x: indicators[x]
)

# 获取数据
if st.sidebar.button("获取数据"):
    with st.spinner("正在获取数据..."):
        df = fetch_fina_data(ts_code)

        if df is not None and not df.empty:
            st.success("数据获取成功！")

            # 数据预览
            st.subheader("原始数据预览")
            st.dataframe(df.head())

            # 按年统计
            st.subheader("年度财务指标分析")
            yearly_data = create_yearly_analysis(df, indicators)
            st.dataframe(yearly_data)

            # 年度图表
            for indicator in selected_indicators:
                fig = plot_indicator(yearly_data, 'year', indicator,
                                  f"{ts_code} 年度趋势", indicators[indicator])
                st.plotly_chart(fig)

            # 按季度统计
            st.subheader("季度财务指标分析")
            quarterly_data = create_quarterly_analysis(df, indicators)
            st.dataframe(quarterly_data)

            # 季度图表
            for indicator in selected_indicators:
                fig = plot_indicator(quarterly_data, 'period', indicator,
                                  f"{ts_code} 季度趋势", indicators[indicator])
                st.plotly_chart(fig)

            # 分析总结
            st.subheader("财务指标分析总结")
            for indicator in selected_indicators:
                latest = yearly_data[indicator].iloc[-1]
                earliest = yearly_data[indicator].iloc[0]
                change = ((latest - earliest) / earliest * 100) if earliest != 0 else 0
                st.write(f"{indicators[indicator]}: "
                        f"最新值 {latest:.2f}, "
                        f"变化率 {change:.2f}%")
        else:
            st.warning("未获取到数据，请检查股票代码或网络连接")

# 添加说明
st.sidebar.markdown("""
### 使用说明
1. 输入正确的股票代码（如600000.SH）
2. 选择要分析的财务指标
3. 点击"获取数据"按钮查看结果
4. 支持年度和季度分析视图
""")


