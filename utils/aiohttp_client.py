import asyncio
import traceback
from typing import Dict

from aiclient.utils import JsonUtil, LogUtil
import aiohttp


class AIOHttpClient(object):

    def __init__(self, base_url: str, retry_times: int = 3, headers: Dict = None, print_log: bool = False,
                 encoding: str = 'utf-8', timeout: int = 30):
        """
        :param base_url: 基础url
        :param retry_times: 重试次数
        :param headers: 请求头
        :param print_log: 是否打印日志
        """
        if not base_url.startswith('http://') or not base_url.startswith('https://'):
            base_url = 'http://' + base_url
        self.base_url = base_url
        self.session = aiohttp.ClientSession()

        self.headers = {}
        if headers:
            self.headers = headers
        self.headers['Content-Type'] = 'application/json; charset=utf8'
        self.print_log = print_log
        self.encoding = encoding
        self.timeout = timeout
        self.retry_times = retry_times

    async def do_request(self, url: str, data: dict, timeout: int = None):
        self.__log("请求参数:{},{}".format(url, JsonUtil.serialize(data, indent=None)))
        res = None
        try:
            async with self.session.post(url, headers=self.headers, json=data,
                                          timeout=(timeout if timeout is not None else self.timeout)) as res:
                self.__log("返回结果:{},{}".format(url, await res.text(encoding=self.encoding)))
        except:
            self.__log("执行出错:\n{}".format(traceback.format_exc()), 'ERROR')
            return res
        return JsonUtil.deserialize(await res.text(encoding=self.encoding))

    def __log(self, content: str, level: str = 'INFO'):
        if self.print_log:
            if level is 'INFO':
                LogUtil.log(content)
            elif level is 'WARN':
                LogUtil.warning(content)
            elif level is 'DEBUG':
                LogUtil.debug(content)
        if level is 'ERROR':
            LogUtil.error(content)

