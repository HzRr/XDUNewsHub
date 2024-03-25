import datetime


class NewsData:
    timestamp: int
    url: str
    title: str

    def __str__(self):
        text = f"timestamp:\t{self.timestamp}\n" \
               f"url:\t\t{self.url}\n" \
               f"title:\t\t{self.title}\n"

        return text
