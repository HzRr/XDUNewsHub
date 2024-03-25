import logging
from logging.handlers import RotatingFileHandler
import os

from config import DEFAULT_LOG_NAME, LOG_LEVEL, LOG_PATH, SAVE_LOG


# ANSI颜色代码
class LogColors:
    GREEN = "\033[32m"
    BLUE = "\033[34m"  # 天蓝色
    WHITE = "\033[37m"
    RESET = "\033[0m"
    LEVEL_COLORS = {
        logging.DEBUG: "\033[36m",  # 淡蓝色
        logging.INFO: "\033[32m",  # 绿色
        logging.WARNING: "\033[33m",  # 黄色
        logging.ERROR: "\033[31m",  # 红色
        logging.CRITICAL: "\033[35m",  # 紫红色
    }


class ColorFormatter(logging.Formatter):
    def __init__(self, fmt, datefmt=None):
        super().__init__(fmt, datefmt)
        self.fmt = fmt
        self.datefmt = datefmt

    def format(self, record):
        # 使用颜色代码格式化各个部分
        record.asctime = LogColors.GREEN + self.formatTime(record, self.datefmt) + LogColors.RESET
        levelname_color = LogColors.LEVEL_COLORS.get(record.levelno, LogColors.WHITE)
        record.levelname = levelname_color + record.levelname + LogColors.RESET
        record.name = LogColors.BLUE + record.name + LogColors.RESET
        record.msg = LogColors.WHITE + record.msg + LogColors.RESET

        # 使用父类方法完成最终的格式化
        formatted_record = super().format(record)

        return formatted_record


def get_logger(
        name: str = DEFAULT_LOG_NAME,
        level: int = LOG_LEVEL,
        console_format: str = (f'{LogColors.GREEN}%(asctime)s{LogColors.RESET} '
                               f'{LogColors.WHITE}[{LogColors.RESET}%(levelname)s{LogColors.WHITE}]{LogColors.RESET} '
                               f'%(name)s {LogColors.WHITE}|{LogColors.RESET} %(message)s'),
        file_path: str = LOG_PATH,
        file_mode: str = 'a',
        file_level: int = logging.INFO,
        file_encoding: str = 'utf-8',
        file_format: str = f'%(asctime)s [%(levelname)s] %(name)s | %(message)s',
        console_datefmt: str = '%Y-%m-%d %H:%M:%S',
        file_datefmt: str = '%Y-%m-%d %H:%M:%S',
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if SAVE_LOG is True:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file_handler = RotatingFileHandler(file_path, mode=file_mode, encoding=file_encoding, backupCount=5,
                                           maxBytes=10 * 1024 * 1024)
        file_handler.setLevel(file_level)
        file_formatter = logging.Formatter(file_format, datefmt=file_datefmt)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # 设置控制台日志，使用颜色格式化
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = ColorFormatter(console_format, datefmt=console_datefmt)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.propagate = False
    return logger
