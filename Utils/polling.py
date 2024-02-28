from Spiders import spiders
from Struct import SpiderResponse
from config import POLLING_INTERVAL, MAX_RETRY_CNT


def handle_response(response: SpiderResponse):
    if response.quantity_of_news() == 0:
        return




def execute_spider(spider):
    retry_cnt = 0
    while retry_cnt <= MAX_RETRY_CNT:
        response = SpiderResponse()
        spider(response)

        if response.code != 200:
            retry_cnt += 1
            continue
        else:
            handle_response(response)
            break


def polling():
    for spider in spiders:
        execute_spider(spider)
