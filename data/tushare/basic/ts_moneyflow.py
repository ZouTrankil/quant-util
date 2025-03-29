#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/3/16.
@author: Air.Zou
"""
from utils.global_config import DataSource


def get_industry_moneyflow(start_date, end_date):
    """
    获取指定日期范围内的板块资金流向数据
    参数:
        start_date (str): 开始日期（格式为 YYYYMMDD）
        end_date (str): 结束日期（格式为 YYYYMMDD）
    返回:
        DataFrame: 包含板块资金流向的数据
    """
    try:
        # 调用 moneyflow_ind_ths 接口获取数据
        data = DataSource.tushare_pro.moneyflow_ind_ths(start_date=start_date, end_date=end_date)
        return data
    except Exception as e:
        print(f"获取数据失败：{e}")
        return None

def get_stock_moneyflow(symbol, start_date:str = None, end_date:str = None) -> float: # type: ignore
    # df = pro.moneyflow(ts_code=symbol, start_date=start_date, end_date=end_date)
    df = DataSource.tushare_pro.moneyflow_ths(ts_code=symbol, start_date=start_date, end_date=end_date)
    # 计算总流入和总流出
    # bs = df['buy_sm_amount'].sum()
    # bm = df['buy_md_amount'].sum()
    # bl = df['buy_lg_amount'].sum()
    # 计算总流入和总流出
    #净流入
    return df['net_amount'].sum()
# 主程序
if __name__ == "__main__":
    start_date = '20250314'
    end_date = None

    # 获取板块资金流向数据
    # data = get_industry_moneyflow(start_date, end_date)

    # 分析并筛选净流入总和为正数的板块
    # positive_inflow_data = analyze_and_sum_net_inflow(data)

    # print(positive_inflow_data)

    r = get_stock_moneyflow("600519.sh", start_date)
    print(r)
