from Struct import SpiderResponse


def polling_request(spider):
    response = SpiderResponse()
    spider(response)

    print(response)
    for news_data in response.news_data_list:
        print(news_data)
