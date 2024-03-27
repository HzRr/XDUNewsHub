from typing import List

from .NewsData import NewsData


class SpiderResponse:
    code: int = 200
    news_data_list: List[NewsData] = []
    saved_info: str = ""        # 上一个会话保存的信息，用于确认下一次爬取的起点

    def quantity_of_news(self) -> int:
        return len(self.news_data_list)

    def __str__(self) -> str:
        text = (f"code:             {self.code}\n"
                f"saved_info:       {self.saved_info}\n"
                f"quantity_of_news: {self.quantity_of_news()}\n"
                )

        return text
