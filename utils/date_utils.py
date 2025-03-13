#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/03/2025.
@author: Air.Zou
"""

import datetime


def get_current_date_str():
    current_date = datetime.date.today()
    formatted_date = current_date.strftime("%Y%m%d")
    return formatted_date


if __name__ == '__main__':
    print(get_current_date_str())
