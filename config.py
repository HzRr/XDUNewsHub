import logging
import time

import pymysql


# 轮询配置
POLLING_INTERVAL: int = 600             # 轮询间隔
MAX_RETRY_CNT: int = 3                  # 最大重试次数

# 数据库配置
MYSQL_CONFIG: dict = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '12345',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

DEFAULT_LOG_NAME: str = "XDUNewsHub"            # 默认日志名称
LOG_LEVEL: int = logging.DEBUG                   # 默认日志等级
SAVE_LOG: bool = True                           # 是否写入文件
LOG_PATH: str = f"logs/{time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())}.log"   # log文件路径

# api.py
API_HOST: str = "0.0.0.0"
API_PORT: int = 5000
API_URL: str = f"http://localhost:{API_PORT}"
GET_NEWS_API_URL: str = f"{API_URL}/get_news"

# app.py
PAGE_NEWS_LIMIT: int = 15
