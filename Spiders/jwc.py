import time
from typing import List

import requests
from lxml import etree

from Struct import NewsData, SpiderResponse
from Utils.database import news_exists


src_url = "https://jwc.xidian.edu.cn/tzgg.htm"
site_url = "https://jwc.xidian.edu.cn/"
site_name = "教务处"

html: etree.Element


def formatted_time2timestamp(formatted_time: str) -> int:
    return int(time.mktime(time.strptime(formatted_time, "%Y-%m-%d")))


def crawl_page(url: str) -> List[NewsData]:
    resp_html = requests.get(url).content.decode("utf8")

    global html
    html = etree.HTML(resp_html)
    news_list = html.xpath("//div[@class='list']//li/a")
    news_data_list = []
    for news in news_list:
        news_data = NewsData()
        tree = etree.ElementTree(news)

        update_time = tree.xpath("//span/text()")[0]

        news_data.timestamp = formatted_time2timestamp(update_time)
        news_data.url = site_url + news.attrib["href"]
        news_data.title = news.attrib["title"]

        news_data_list.append(news_data)

    return news_data_list


def crawl_next_page() -> List[NewsData]:
    next_page_url = site_url + html.xpath("//a[@class='Next']/@href")[0]
    return crawl_page(next_page_url)


def is_enough(news_data_list: List[NewsData], last_order: int) -> bool:
    for news_data in news_data_list:
        order = get_order(news_data.url)
        if order <= last_order:
            return True

    return False


def get_order(url: str) -> int:
    return int(url.split("/")[-1].split(".")[0])


def add_news_data_list(news_data_list: List[NewsData], response: SpiderResponse) -> None:
    for news_data in news_data_list:
        response.news_data_list.append(news_data)
    return


def remove_existing_news_data(response: SpiderResponse) -> None:
    news_data_list = []
    for news_data in response.news_data_list:
        if news_exists(news_data.url) is False:
            news_data_list.append(news_data)
    response.news_data_list = news_data_list
    return


def jwc_spider(response: SpiderResponse) -> None:
    response.site_name = site_name
    response.site_url = site_url

    news_data_list = crawl_page(src_url)
    add_news_data_list(news_data_list, response)
    last_order = int(response.saved_info) if response.saved_info != "" else 13012
    while is_enough(news_data_list, last_order) is False:
        news_data_list = crawl_next_page()
        add_news_data_list(news_data_list, response)

    response.saved_info = str(get_order(response.news_data_list[0].url))
    remove_existing_news_data(response)

    return
