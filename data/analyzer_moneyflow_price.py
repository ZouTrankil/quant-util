#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 16/03/2025.
@author: Air.Zou
"""
import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np
import akshare as ak

# 数据准备
df = ak.stock_zh_a_tick_tx_js(symbol="sz002261")
print(df)

'''
      成交时间   成交价格  价格变动    成交量       成交金额   性质
0     09:25:00  34.10  0.00  15223   51910430   卖盘
1     09:30:00  34.12  0.02   3423   11679547   买盘
'''

# 特征工程
df['成交量标准化'] = (df['成交量'] - df['成交量'].mean()) / df['成交量'].std()
df['价格变动绝对值'] = df['价格变动'].abs()
total_amount = df['成交金额'].sum()
df['买卖金额比例'] = np.where(df['性质'] == '买盘', df['成交金额'] / total_amount, 0)

# 选择特征
features = ['成交量标准化', '价格变动绝对值', '买卖金额比例']
X = df[features]

# 训练Isolation Forest模型
model = IsolationForest(contamination=0.2, random_state=42)  # 假设20%为异常
df['异常分数'] = model.fit_predict(X)

# 筛选异常交易（-1表示异常）
anomalies = df[df['异常分数'] == -1]

# 输出结果
print("疑似主力资金的异常交易：")
print(anomalies[['成交时间', '成交量', '成交价格', '价格变动', '性质']])

# 策略建议
if not anomalies.empty:
    anomaly_inflow = anomalies[anomalies['性质'] == '买盘']['成交金额'].sum()
    print(f"疑似主力资金流入金额: {anomaly_inflow} 元")
    print("策略建议：检测到异常买盘行为，可能是主力资金操作，建议进一步分析或关注。")
else:
    print("未检测到异常交易。")

df.to_csv('zh_a_tick_tx_js.csv')
anomalies.to_csv('zh_a_tick_tx_js_anomalies.csv')