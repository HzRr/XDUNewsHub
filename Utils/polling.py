import time

import pymysql.err

from Spiders import spiders
from Struct import SpiderResponse
from Utils.logger import get_logger
from Utils.database import add_news_data
from config import POLLING_INTERVAL, MAX_RETRY_CNT


def load_saved_info(response: SpiderResponse, spider_name: str) -> None:
    logger = get_logger(name='read_saved_info')

    logger.debug(f'spider: [{spider_name}] try to reads saved info')
    with open(f'data/{spider_name}.txt', 'a+') as fp:
        # reseek to the start of file
        fp.seek(0)
        response.saved_info = fp.read()
    logger.debug(f'spider: [{spider_name}] reads saved info:\n{response.saved_info}')


def dump_saved_info(response: SpiderResponse, spider_name: str) -> None:
    logger = get_logger(name='dump_saved_info')

    logger.debug(f'spider: [{spider_name}] dumps saved info:\n{response.saved_info}')
    with open(f'data/{spider_name}.txt', 'w') as fp:
        fp.write(response.saved_info)
    logger.debug(f'spider: [{spider_name}] dumps saved info successfully!')


def handle_response(spider_name: str, response: SpiderResponse) -> None:
    logger = get_logger(name='handle_response')

    exists_cnt = 0
    for news_data in response.news_data_list:
        try:
            add_news_data(news_data, response.site_name, response.site_url)
        except pymysql.err.IntegrityError:
            exists_cnt += 1
            logger.error(f'spider: [{spider_name}] news: [{news_data.url}] already exists')

    dump_saved_info(response, spider_name)

    logger.info(f'spider: [{spider_name}] crawls {response.quantity_of_news() - exists_cnt} news')


def execute_spider(spider: callable) -> None:
    logger = get_logger(name='execute')
    spider_name = spider.__name__
    retry_cnt = 0

    while retry_cnt <= MAX_RETRY_CNT:
        response = SpiderResponse()
        load_saved_info(response, spider_name)
        spider(response)

        if response.code != 200:
            logger.error(f'execute spider: [{spider_name}] failed, retry {retry_cnt}/{MAX_RETRY_CNT}')
            retry_cnt += 1
            continue
        else:
            handle_response(spider_name, response)
            logger.info(f'execute spider: [{spider_name}] success')
            return


def polling():
    logger = get_logger(name='polling')
    while True:
        for spider in spiders:
            execute_spider(spider)
        logger.info(f'polling ends, stop for {POLLING_INTERVAL} seconds')
        time.sleep(POLLING_INTERVAL)
