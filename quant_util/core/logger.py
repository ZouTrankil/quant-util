"""
日志模块

提供日志记录功能，支持控制台和文件输出，以及不同级别的日志过滤。
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Optional, Dict, Any, Union, List, ClassVar, cast
import datetime
import inspect


class LoggerConfig:
    """日志配置类"""

    def __init__(
        self,
        log_dir: str = "./logs",
        app_name: str = "app",
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        use_time_rotate: bool = False,
        when: str = 'D',
        format_str: str = "[%(asctime)s][%(levelname)s][%(name)s] %(message)s"
    ):
        """初始化日志配置

        Args:
            log_dir (str, optional): 日志目录. 默认为"./logs".
            app_name (str, optional): 应用名称. 默认为"app".
            console_level (int, optional): 控制台日志级别. 默认为logging.INFO.
            file_level (int, optional): 文件日志级别. 默认为logging.DEBUG.
            max_bytes (int, optional): 日志文件最大字节数. 默认为10MB.
            backup_count (int, optional): 备份文件数量. 默认为5.
            use_time_rotate (bool, optional): 是否使用时间轮转. 默认为False.
            when (str, optional): 轮转时间单位(S/M/H/D/W0-W6). 默认为'D'.
            format_str (str, optional): 日志格式. 默认为"[%(asctime)s][%(levelname)s][%(name)s] %(message)s".
        """
        self.log_dir = log_dir
        self.app_name = app_name
        self.console_level = console_level
        self.file_level = file_level
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.use_time_rotate = use_time_rotate
        self.when = when
        self.format_str = format_str

        # 创建日志目录
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)


class LoggerFactory:
    """日志工厂，用于创建和管理日志实例"""

    _instance: ClassVar[Optional['LoggerFactory']] = None
    _loggers: ClassVar[Dict[str, logging.Logger]] = {}
    _config: ClassVar[LoggerConfig] = LoggerConfig()  # 默认配置

    @classmethod
    def initialize(cls, config: Optional[LoggerConfig] = None) -> None:
        """初始化日志工厂

        Args:
            config (Optional[LoggerConfig], optional): 日志配置. 默认为None(使用默认配置).
        """
        if cls._instance is None:
            cls._instance = cls()

        if config is not None:
            cls._config = config

    @classmethod
    def get_logger(cls, name: Optional[str] = None) -> logging.Logger:
        """获取日志实例

        如果不指定name，则使用调用方模块的名称

        Args:
            name (Optional[str], optional): 日志名称. 默认为None.

        Returns:
            logging.Logger: 日志实例
        """
        if cls._instance is None:
            cls.initialize()

        if name is None:
            # 获取调用方模块名称
            frame = inspect.currentframe()
            if frame and frame.f_back:
                module = inspect.getmodule(frame.f_back)
                name = module.__name__ if module else "unknown"
            else:
                name = "unknown"

        if name not in cls._loggers:
            logger = logging.getLogger(name)

            if not logger.handlers:
                cls._configure_logger(logger)

            cls._loggers[name] = logger

        return cls._loggers[name]

    @classmethod
    def _configure_logger(cls, logger: logging.Logger) -> None:
        """配置日志实例

        Args:
            logger (logging.Logger): 日志实例
        """
        logger.setLevel(logging.DEBUG)  # 设置为最低级别，让handler决定过滤

        # 创建格式化器
        formatter = logging.Formatter(cls._config.format_str)

        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(cls._config.console_level)
        logger.addHandler(console_handler)

        # 创建文件处理器
        log_file = os.path.join(
            cls._config.log_dir,
            f"{cls._config.app_name}.log"
        )

        if cls._config.use_time_rotate:
            file_handler = TimedRotatingFileHandler(
                log_file,
                when=cls._config.when,
                backupCount=cls._config.backup_count
            )
        else:
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=cls._config.max_bytes,
                backupCount=cls._config.backup_count
            )

        file_handler.setFormatter(formatter)
        file_handler.setLevel(cls._config.file_level)
        logger.addHandler(file_handler)


# 预定义的日志获取函数
def get_logger(name: Optional[str] = None) -> logging.Logger:
    """获取日志实例

    Args:
        name (Optional[str], optional): 日志名称. 默认为None(使用调用方模块名称).

    Returns:
        logging.Logger: 日志实例
    """
    return LoggerFactory.get_logger(name)


def set_log_config(
    log_dir: str = "./logs",
    app_name: str = "app",
    console_level: Union[int, str] = logging.INFO,
    file_level: Union[int, str] = logging.DEBUG,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    use_time_rotate: bool = False,
    when: str = 'D'
) -> None:
    """设置日志配置

    Args:
        log_dir (str, optional): 日志目录. 默认为"./logs".
        app_name (str, optional): 应用名称. 默认为"app".
        console_level (Union[int, str], optional): 控制台日志级别. 默认为logging.INFO.
        file_level (Union[int, str], optional): 文件日志级别. 默认为logging.DEBUG.
        max_bytes (int, optional): 日志文件最大字节数. 默认为10MB.
        backup_count (int, optional): 备份文件数量. 默认为5.
        use_time_rotate (bool, optional): 是否使用时间轮转. 默认为False.
        when (str, optional): 轮转时间单位(S/M/H/D/W0-W6). 默认为'D'.
    """
    # 处理字符串级别
    console_level_int: int = logging.INFO
    file_level_int: int = logging.DEBUG

    if isinstance(console_level, int):
        console_level_int = console_level
    elif isinstance(console_level, str):
        console_level_int = getattr(logging, console_level.upper())

    if isinstance(file_level, int):
        file_level_int = file_level
    elif isinstance(file_level, str):
        file_level_int = getattr(logging, file_level.upper())

    config = LoggerConfig(
        log_dir=log_dir,
        app_name=app_name,
        console_level=console_level_int,
        file_level=file_level_int,
        max_bytes=max_bytes,
        backup_count=backup_count,
        use_time_rotate=use_time_rotate,
        when=when
    )

    LoggerFactory.initialize(config)
