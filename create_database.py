import pymysql.cursors

from config import MYSQL_CONFIG
from Utils.logger import get_logger


connection = pymysql.connect(**MYSQL_CONFIG)
logger = get_logger(name="create_database")

try:
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS news_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        # 检查表news_data是否存在，如果不存在则创建
        cursor.execute("USE news_hub;")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `news_data` (
                `url` VARCHAR(127) NOT NULL,
                `title` VARCHAR(255) NOT NULL,
                `timestamp` DATETIME NULL DEFAULT NULL,
                `site_name` VARCHAR(63) NULL DEFAULT NULL,
                `site_url` VARCHAR(127) NULL DEFAULT NULL,
                PRIMARY KEY (`url`)
            ) COLLATE='utf8mb4_unicode_ci';
        """)
        # 提交以确保MySQL创建数据库和表
        connection.commit()

        logger.info('Database created successfully')
finally:
    connection.close()
