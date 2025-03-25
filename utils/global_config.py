#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/03/2025.
@author: Air.Zou
"""
import tushare as ts
import logging
import akshare as ak


class BaseConfig:
    """
    可以自行继承 BaseConfig 定义自己的配置类
    """

    """ 配置前缀 """
    prefix = ''

    def __init__(self, **kwargs):
        """
        可以直接通过构造器赋值或者通过 attitude 给配置赋值，其中传入的 kwargs 必须与类静态变量名一致才会生效
        example:
            Config(prefix='')
        or:
            config = Config()
            config.prefix = ''
        :param kwargs:
        """

        def filter_func(item: str):
            if item.startswith('__') and item.endswith('__'):
                return False
            else:
                return True

        custom_items = list(filter(filter_func, dir(self)))

        illegal_key = []
        for k in kwargs:
            if k not in custom_items:
                illegal_key.append(k)
        if len(illegal_key) > 0:
            logging.getLogger(__name__).warning('检测到无效 key，请检查：{}'.format(illegal_key))

        for k in custom_items:
            if k in kwargs:
                self.__setattr__(k, kwargs[k])
            else:
                self.__setattr__(k, self.__getattribute__(k))


class DataSource(BaseConfig):
    tushare_pro = ts.pro_api(token='2876ea85cb005fb5fa17c809a98174f2d5aae8b1f830110a5ead6211')