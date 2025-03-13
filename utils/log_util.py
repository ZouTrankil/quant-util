# coding:utf-8
import os
import sys

from loguru import logger


class LogUtil(object):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # 项目路径
    rootPath = os.path.split(BASE_DIR)[0]
    path = os.path.join(rootPath, 'log')
    # 关键代码，将堆栈上调一级，能够获取到 LogUtil 上级的调用者
    _logger = logger.opt(depth=1)
    _logger.remove()
    _logger.add(sys.stderr, level='DEBUG' if sys.gettrace() else 'INFO')
    _logfile_enabled = True

    @staticmethod
    def debug(msg):
        LogUtil._logger.debug(msg)

    @staticmethod
    def info(msg):
        LogUtil._logger.info(msg)

    @staticmethod
    def warning(msg):
        LogUtil._logger.warning(msg)

    @staticmethod
    def error(msg):
        LogUtil._logger.error(msg)

    @staticmethod
    def critical(msg):
        LogUtil._logger.critical(msg)

    @staticmethod
    def log(msg):
        LogUtil._logger.info(msg)

    @staticmethod
    def change_log_level(level: str):
        LogUtil._logger.level(level)

    @staticmethod
    def log_file_enable(logpath: str = 'console'):
        if LogUtil._logfile_enabled is False:
            LogUtil._logger.add(logpath + '_{time}.log', rotation="200MB", encoding="utf-8", enqueue=True,
                                compression="zip", retention="10 days")

if __name__ == '__main__':
    LogUtil.log_file_enable()
    LogUtil.debug('info1')
    LogUtil.warning('info1')
    LogUtil.debug('info2')
    LogUtil.critical('info3')
    LogUtil.info('info3')
    LogUtil.error('info3')
