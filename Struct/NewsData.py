import datetime


class NewsData:
    url: str
    title: str
    timestamp: int
    site_name: str
    site_url: str

    def __init__(self, site_name: str | None = None, site_url: str | None = None):
        self.site_name = site_name
        self.site_url = site_url

    def __str__(self):
        text = (f"url:       {self.url}\n"
                f"title:     {self.title}\n"
                f"timestamp: {self.timestamp}\n"
                f"site_name: {self.site_name}"
                f"site_url:  {self.site_url}")

        return text
