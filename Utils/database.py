import pymysql

from Struct import NewsData
from config import MYSQL_CONFIG


def get_connection() -> pymysql.connections.Connection:
    return pymysql.connect(database='news_hub', **MYSQL_CONFIG)


def query_by_url(url: str) -> list:
    sql = "SELECT url, title, UNIX_TIMESTAMP(datetime), site_name, site_url FROM news_data where url='%s'" % url
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()


def select_news_data(filter_str: str, order_str: str, limit_str: str) -> list[dict]:
    sql = ("SELECT url, title, UNIX_TIMESTAMP(datetime), site_name, site_url "
           "FROM news_data WHERE %s ORDER BY %s LIMIT %s" %
           (filter_str, order_str, limit_str))
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()


def add_news_data(news_data: NewsData) -> int:
    sql = ("INSERT INTO news_data (url, title, datetime, site_name, site_url) "
           "VALUES ('%s', '%s', FROM_UNIXTIME(%s), '%s', '%s')" %
           (news_data.url, news_data.title, news_data.timestamp, news_data.site_name, news_data.site_url))
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            return cursor.rowcount


def update_news_data(news_data: NewsData) -> int:
    sql = ("UPDATE news_data SET title='%s', datetime=FROM_UNIXTIME(%s), site_name='%s', site_url='%s' "
           "WHERE url='%s'" %
           (news_data.title, news_data.timestamp, news_data.site_name, news_data.site_url, news_data.url))
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


def is_content_sql_injection(content: str) -> bool:
    return any(char in content for char in "'\"`#-")


def count_news_data() -> int:
    sql = "SELECT COUNT(*) FROM news_data"
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()['COUNT(*)']
