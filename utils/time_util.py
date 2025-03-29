import signal
import sys
import time
from multiprocessing import Process, Event

import requests

from .log_util import LogUtil


class TimeUtil:
    @staticmethod
    def get_current_time():
        return int(round(time.time() * 1000))


class RepeatedTimer(object):
    """
    循环定时任务
    """

    @staticmethod
    def worker(interval, function, stop_event, kwargs):
        # 定时执行任务，直到 stop_event 被设置
        while not stop_event.is_set():
            function(**kwargs)
            time.sleep(interval)

    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args

        # 创建停止事件
        self.stop_event = Event()
        self.kwargs = kwargs
        self.kwargs['stop_event'] = self.stop_event
        self.process = Process(target=RepeatedTimer.worker, args=(interval, function, self.stop_event, kwargs))
        self.process.daemon = True
        self.process.start()

    def stop(self):
        # 触发停止事件并等待进程结束
        self.stop_event.set()
        self.process.join()


class SignalHandledTimer(RepeatedTimer):
    """
    带信号处理的循环定时任务
    """

    def __init__(self, interval, function, *args, **kwargs):
        super().__init__(interval, function, *args, **kwargs)
        signal.signal(signal.SIGINT, self.signal_handler)  # Handle Ctrl+C
        signal.signal(signal.SIGTERM, self.signal_handler)  # Handle termination signal

    def signal_handler(self, signum, frame):
        LogUtil.warning("接收到关闭信号，正在停止定时任务...")
        self.stop()
        sys.exit(0)


def func(**kwargs):
    print("执行中...\n")
    print(requests.get("https://www.baidu.com").content)

    # 通过 kwargs 获取 stop_event 并触发停止
    stop_event = kwargs.get('stop_event')
    if stop_event:
        print("触发停止事件")
        stop_event.set()


class Example:
    def __init__(self):
        self.timer = None

    def start(self):
        # 创建定时器并传入 func
        self.timer = SignalHandledTimer(5, func)

        # 让定时器运行一段时间
        time.sleep(20)
        self.timer.stop()


if __name__ == '__main__':
    e = Example()
    e.start()
