import pymysql

from Struct import NewsData
from config import MYSQL_CONFIG


def get_connection() -> pymysql.connections.Connection:
    return pymysql.connect(database='news_hub', **MYSQL_CONFIG)


def query(url: str = None, params: tuple | list | dict | None = None) -> list:
    sql = "SELECT url, title, timestamp FROM news_data where url='%s'" % url
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()


def add_news_data(news_data: NewsData) -> int:
    sql = ("INSERT INTO news_data (url, title, timestamp) VALUES ('%s', '%s', FROM_UNIXTIME(%s))" %
           (news_data.url, news_data.title, news_data.timestamp))
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            return cursor.rowcount


def update_news_data(news_data: NewsData) -> int:
    sql = ("UPDATE news_data SET title='%s', timestamp=FROM_UNIXTIME(%s) WHERE url='%s'" %
           (news_data.title, news_data.timestamp, news_data.url))
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            return cursor.rowcount


def delete_news_data(url: str) -> int:
    sql = "DELETE FROM news_data WHERE url='%s'" % url
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            cursor.execute(sql)
            conn.commit()
            return cursor.rowcount


def news_exists(url: str) -> bool:
    sql = "SELECT url FROM news_data WHERE url='%s'" % url
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.rowcount > 0
