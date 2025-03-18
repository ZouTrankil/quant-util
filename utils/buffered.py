import signal
import sys
import threading
import time
from typing import Callable, List, Any

from aiclient.utils.log_util import LogUtil


class Buffered:

    @staticmethod
    def signal_handler(signum, frame):
        LogUtil.warning("接收到关闭信号...")
        buffer.close()
        sys.exit(0)

    def __init__(self, max_size: int, max_second_timeout: int,
                 flush_callback: Callable[[List[Any]], None] or Callable[[List[Any]], None]):
        self.buffer = []
        self.max_size = max_size
        self.max_second_timeout = max_second_timeout
        self.flush = flush_callback
        self.lock = None
        self.timer = None
        signal.signal(signal.SIGINT, Buffered.signal_handler)
        signal.signal(signal.SIGTERM, Buffered.signal_handler)

    def start_timer(self):
        """启动定时器"""
        if not self.timer or not self.timer.is_alive():
            self.timer: threading.Timer = threading.Timer(self.max_second_timeout, self.flush_timer)
            self.timer.start()

    def stop_timer(self):
        if self.timer and self.timer.is_alive():
            self.timer.cancel()

    def flush_timer(self):
        """定时器触发的刷新操作"""
        with self.lock:
            if self.buffer:
                current_buffer = self.buffer.copy()  # 复制当前缓冲区
                self.buffer = []  # 立即清空缓冲区
                LogUtil.debug(f'执行定时刷新，缓冲区长度：{len(current_buffer)}')
                self.flush(current_buffer)  # 处理复制的数据
                self.stop_timer()

    def write(self, data):
        if self.lock is None:
            self.lock = threading.Lock()
        """写入数据"""
        with self.lock:
            self.buffer.append(data)
            # 仅在即将溢出时强制刷新
            if len(self.buffer) >= self.max_size:
                current_buffer = self.buffer.copy()
                self.buffer = []
                LogUtil.debug(f'缓冲区已满，执行刷新')
                self.flush(current_buffer)
            else:
                # 还没有满就开启定时任务用于超时上报
                self.start_timer()

    def close(self):
        """安全关闭"""
        if self.timer:
            self.stop_timer()
        with self.lock:
            if self.buffer:
                self.flush(self.buffer)
                self.buffer = []


if __name__ == '__main__':
    def callback(data):
        if data is not None and len(data) > 0:
            LogUtil.debug(f'写入数据，长度{len(data)},数据：{data}')


    buffer = Buffered(5, 3, callback)
    index = 0
    while True:
        index += 1
        buffer.write(f"test{index}")
        time.sleep(1)
