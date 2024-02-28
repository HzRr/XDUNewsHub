from typing import List

from .NewsData import NewsData


class SpiderResponse:
    code: int = 200
    news_data_list: List[NewsData] = []
    saved_info: str = ""        # 上一个会话保存的信息，用于确认下一次爬取的起点
    src_site_name: str = ""
    src_site_url: str = ""

    def quantity_of_news(self) -> int:
        return len(self.news_data_list)

    def __str__(self) -> str:
        text = f"code:\t\t\t\t{self.code}\n" \
               f"saved_info:\t\t\t{self.saved_info}\n" \
               f"quantity_of_news:\t{self.quantity_of_news()}\n" \
               f"src_site_name:\t\t{self.src_site_name}\n" \
               f"src_site_url:\t\t{self.src_site_url}\n"

        return text
