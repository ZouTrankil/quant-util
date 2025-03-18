import traceback
from typing import Dict, Callable

import requests
from requests.adapters import HTTPAdapter

from aiclient.utils import JsonUtil, LogUtil


class HttpClient(object):

    def __init__(self, base_url: str, retry_times: int = 3, headers: Dict = None, print_log: bool = False, encoding: str='utf-8', timeout: int = 30):
        """
        :param base_url: 基础url
        :param retry_times: 重试次数
        :param headers: 请求头
        :param print_log: 是否打印日志
        """
        if not base_url.startswith('http://') or not base_url.startswith('https://'):
            base_url = 'http://' + base_url
        self.base_url = base_url
        self.session = requests.session()
        self.session.mount('http://', HTTPAdapter(max_retries=retry_times))
        self.session.mount('https://', HTTPAdapter(max_retries=retry_times))

        self.headers = {}
        self.headers['Content-Type'] = 'application/json; charset=utf8'
        if headers:
            self.headers.update(headers)
        self.print_log = print_log
        self.encoding = encoding
        self.timeout = timeout

    def do_request(self, url: str, data: dict, timeout: int = None):
        self.__log_func(lambda: '请求地址:{},请求参数:{}'.format(url, JsonUtil.serialize(data, None)))
        res = None
        try:
            res = self.session.post(url, headers=self.headers, json=data,
                                    timeout=(timeout if timeout is not None else self.timeout))
            self.__log_func(lambda: "返回结果:{},{}".format(url, res.text))
        except:
            self.__log_func(lambda: "执行出错:\n{}".format(traceback.format_exc()), 'ERROR')
            return res
        return JsonUtil.deserialize(res.text)

    def __log(self, content: str, level: str = 'INFO'):
        if self.print_log:
            if level == 'INFO':
                LogUtil.log(content)
            elif level == 'WARN':
                LogUtil.warning(content)
            elif level == 'DEBUG':
                LogUtil.debug(content)
        if level == 'ERROR':
            LogUtil.error(content)

    def __log_func(self, func: Callable, level: str = 'INFO'):
        if self.print_log:
            self.__log(func(), level)
