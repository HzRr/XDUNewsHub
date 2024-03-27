import datetime


class NewsData:
    url: str
    title: str
    timestamp: int
    site_name: str
    site_url: str

    def __str__(self):
        text = (f"url:       {self.url}\n"
                f"title:     {self.title}\n"
                f"timestamp: {self.timestamp}\n"
                f"site_name: {self.site_name}"
                f"site_url:  {self.site_url}")

        return text
